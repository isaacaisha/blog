import os
import flask
from markupsafe import Markup

# Monkey-patch flask.Markup so flask_ckeditor can import it:
flask.Markup = Markup

from flask import Flask, render_template, redirect, url_for, flash, request, abort
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor   # ← now it will see flask.Markup
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
from flask_gravatar import Gravatar
from flask_migrate import Migrate
from functools import wraps
from datetime import datetime, timezone
from forms import CreatePostForm, RegisterForm, LoginForm, CommentForm


# Set up Flask app
app = Flask(__name__, instance_relative_config=True)

# Secret key
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')

# Database configuration — use blog.db inside the instance folder
# Force DATABASE_URL to instance path if not set
db_path = os.path.join(app.instance_path, 'blog.db')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Ensure instance folder exists
os.makedirs(app.instance_path, exist_ok=True)

# Extensions
# Serve from your local static folder
app.config['CKEDITOR_SERVE_LOCAL'] = True
# Pick one: 'basic', 'standard', or 'full'
app.config['CKEDITOR_PKG_TYPE']   = 'full'
ckeditor = CKEditor(app)
Bootstrap(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

gravatar = Gravatar(app, size=100, rating='g', default='retro',
                    force_default=False, force_lower=False,
                    use_ssl=False, base_url=None)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


# CREATE THE USER TABLE IN DB
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    role     = db.Column(db.String(19), nullable=False, default='user')

    # This will act like a List of BlogPost objects attached to each User.
    # The "author" refers to the author property in the BlogPost class.
    posts = relationship("BlogPost", back_populates="author")

    # ******* Add parent relationship ******* #
    # "comment_author" refers to the comment_author property in the Comment class.
    comments = relationship("Comment", back_populates="comment_author")


# CONFIGURE THE BLOG POST TABLES
class BlogPost(db.Model):
    __tablename__ = "blog_posts"
    id = db.Column(db.Integer, primary_key=True)

    # Create Foreign Key, "users.id" the users refers to the tablename of User.
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    # Create reference to the User object, the "posts" refers to the posts property in the User class.
    author = relationship("User", back_populates="posts")

    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.String(250), nullable=False)

    # *************** Parent Relationship ************* #
    comments = relationship("Comment", back_populates="parent_post")


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)

    # ******* Add child relationship ******* #
    # "users.id" The users refer to the tablename of the Users class.
    # "comments" refers to the comments property in the User class.
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    comment_author = relationship("User", back_populates="comments")

    # *************** Child Relationship ************* #
    post_id = db.Column(db.Integer, db.ForeignKey("blog_posts.id"))
    parent_post = relationship("BlogPost", back_populates="comments")

    text = db.Column(db.Text, nullable=False)


with app.app_context():
    db.create_all()


@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('img/favicon.ico')


# Create admin-only decorator
def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If user is not admin, then return abort with 403 error
        if not current_user.is_authenticated or current_user.role != 'admin':
            return abort(403)
        # Otherwise continue with the route function
        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
def get_all_posts():
    posts = BlogPost.query.all()
    return render_template(
        "index.html",
        all_posts=posts,
        current_user=current_user,
        date=datetime.now(timezone.utc).strftime("%a %d %B %Y")
        )


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST':

        # If user's email already exists
        if User.query.filter_by(email=form.email.data).first():
            print(User.query.filter_by(email=form.email.data).first())
            # Send a flash message
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('login'))

        hash_and_salted_password = generate_password_hash(
            request.form.get('password'),
            method='pbkdf2:sha256',
            salt_length=8
        )

        new_user = User()
        new_user.email = request.form['email']
        new_user.name = request.form['name']
        new_user.password = hash_and_salted_password

        db.session.add(new_user)
        db.session.commit()

        # Log in and authenticate the user after adding details to the database.
        login_user(new_user)

        print(f'New username: {new_user.name}\n email: {new_user.email}\n password: {new_user.password}')

        return redirect(url_for('get_all_posts'))

    return render_template(
        "register.html",
        form=form,
        current_user=current_user,
        date=datetime.now(timezone.utc).strftime("%a %d %B %Y")
        )


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        code = form.secret_code.data

        # Find user by email entered.
        user = User.query.filter_by(email=email).first()

        # Email doesn't exist
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('login'))
        # Password incorrect
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.')
            return redirect(url_for('login'))
        # Email exists and password correct
        else:
            # If they supplied the correct admin code, promote them
            if code and code == 'siisi321' and user.role != 'admin':
                user.role = 'admin'
                db.session.commit()
                flash('🎉 You now have admin access!', 'success')

            login_user(user)
            return redirect(url_for('get_all_posts'))

    return render_template(
        "login.html",
        form=form,
        current_user=current_user,
        date=datetime.now(timezone.utc).strftime("%a %d %B %Y")
        )


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('get_all_posts'))


@app.route("/post/<int:post_id>", methods=["GET", "POST"])
def show_post(post_id):
    form = CommentForm()
    requested_post = BlogPost.query.get(post_id)

    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash("You need to login or register to comment.")
            return redirect(url_for("login"))

        new_comment = Comment(
            text=form.comment_text.data,
            comment_author=current_user,
            parent_post=requested_post
        )
        db.session.add(new_comment)
        db.session.commit()

    return render_template(
        "post.html",
        post=requested_post,
        form=form,
        current_user=current_user,
        date=datetime.now(timezone.utc).strftime("%a %d %B %Y")
        )


@app.route("/about")
def about():
    return render_template(
        "about.html",
        current_user=current_user,
        date=datetime.now(timezone.utc).strftime("%a %d %B %Y")
        )


@app.route("/contact")
def contact():
    return render_template(
        "contact.html",
        current_user=current_user,
        date=datetime.now(timezone.utc).strftime("%a %d %B %Y")
        )


@app.route("/new-post", methods=['GET', 'POST'])
# Mark with decorator
@admin_only
def add_new_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            author=current_user,
            date=datetime.today().strftime("%B %d, %Y")
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("get_all_posts"))
    return render_template(
        "make-post.html",
        form=form,
        current_user=current_user,
        date=datetime.now(timezone.utc).strftime("%a %d %B %Y")
        )


@app.route("/edit-post/<int:post_id>", methods=['GET', 'POST'])
# Mark with decorator
@admin_only
def edit_post(post_id):
    post = BlogPost.query.get(post_id)
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=current_user,
        body=post.body
    )
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.body = edit_form.body.data
        db.session.commit()
        return redirect(url_for("show_post", post_id=post.id))

    return render_template(
        "make-post.html",
        form=edit_form,
        is_edit_post=True,
        current_user=current_user,
        date=datetime.now(timezone.utc).strftime("%a %d %B %Y")
        )


@app.route("/delete/<int:post_id>")
# Mark with decorator
@admin_only
def delete_post(post_id):
    post_to_delete = BlogPost.query.get(post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('get_all_posts'))


@app.route("/delete-comment/<int:comment_id>")
# Mark with decorator
@admin_only
def comment_to_delete(comment_id):
    delete_comment = Comment.query.get(comment_id)
    db.session.delete(delete_comment)
    db.session.commit()
    return redirect(url_for('get_all_posts'))


if __name__ == "__main__":
    app.run(debug=True)
