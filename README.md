# 📝 Flask Blog CMS

A beautiful, responsive blog Content Management System (CMS) built with **Flask**, designed for writers, admins, and commenters. Includes secure user authentication, rich-text editing, and user role-based access.

![Platform Demo](static/img/blog.jpg)

---

## 🚀 Features

* 🧑‍💻 User Authentication (Register/Login/Logout)
* 🔐 Admin-only post management
* 📝 Rich Text Post Creation (CKEditor)
* 💬 Comment system (authenticated users only)
* 🎭 Gravatar integration
* 📜 Flask-WTF for form validation
* 💾 SQLAlchemy ORM + Flask-Migrate for migrations
* 🎨 Bootstrap-styled responsive UI
* 📅 Post date display with time zone awareness

---

## 🛠 Tech Stack

| Tech             | Purpose                         |
| ---------------- | ------------------------------- |
| Flask            | Web framework                   |
| Flask-SQLAlchemy | Database ORM                    |
| Flask-Migrate    | Database migrations             |
| Flask-Login      | User session/auth management    |
| Flask-WTF        | Secure form handling            |
| Flask-CKEditor   | Rich text post editor           |
| Flask-Bootstrap  | Frontend UI styling             |
| Flask-Gravatar   | User avatar support             |
| Alembic          | Schema migrations (via migrate) |
| SQLite           | Default local DB                |

---

## 📁 Project Structure

```
📦 your-project/
├── app.py                # Main app logic
├── templates/            # Jinja2 HTML templates
├── static/               # CSS/JS/Images
├── forms.py              # WTForms
├── instance/
│   └── blog.db           # Local SQLite database
├── requirements.txt      # Python dependencies
└── README.md             # This file
```

---

## 🔧 Installation

### 📦 Requirements

* Python 3.9+
* Virtualenv (recommended)

### ⏳ Setup

```bash
# 1. Clone the repository
git clone https://github.com/isaacaisha/blog.git
cd blog

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set environment variables (optional for dev)
export FLASK_APP=app.py
export FLASK_ENV=development
export SECRET_KEY='your-secret-key'

# 5. Run DB migrations
flask db init
flask db migrate
flask db upgrade

# 6. Run the app
flask run
```

---

## 🛡️ Admin Access

To grant admin privileges, a secret code is used during login:

> 🔑 **Admin Code:** `siisi321`

---

## 📸 Screenshots (optional)

Add screenshots of:

* 📃 Blog listing page
* ✍️ Post editor with CKEditor
* 🧑 Login/Register forms
* 💬 Comment section

---

## 📦 Dependencies

```
Flask==2.3.3
Flask-SQLAlchemy==3.1.1
Flask-Login==0.6.3
Flask-WTF==1.2.2
Flask-CKEditor==1.0.0
Flask-Bootstrap==3.3.7.1
Flask-Gravatar==0.5.0
Flask-Migrate==4.1.0
alembic==1.15.2
bleach==6.0.0
```

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you'd like to change.

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 🧠 Author

**Isaac Aïsha** — *Developer & Designer*
GitHub: [@isaacaisha](https://github.com/isaacaisha)
