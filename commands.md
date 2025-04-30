# blog commands eg.:

sudo systemctl daemon-reload
sudo systemctl restart blog.service
sudo systemctl status blog.service

sudo nginx -t
sudo systemctl restart nginx
sudo systemctl status nginx

sudo systemctl restart postgresql
sudo systemctl status postgresql

sudo journalctl -u blog.service -f

# postgresql
sudo nano /etc/postgresql/16/main/postgresql.conf
sudo nano /etc/postgresql/16/main/pg_hba.conf
# Access postgresql
sudo -u postgres psql

# systemd
sudo nano /etc/systemd/system/blog.service

# nginx
sudo nano /etc/nginx/sites-available/blog.conf

# CREATE SSL CERTIFICATE
sudo dnf install certbot python3-certbot-nginx
sudo certbot --nginx

# link the configuration to enable it
sudo ln -s /etc/nginx/sites-available/blog /etc/nginx/sites-enabled/

sudo certbot certificates
sudo certbot --nginx -d blog.siisi.online -d www.blog.siisi.online
 sudo certbot --nginx \
  -d blog.siisi.online -d www.blog.siisi.online \
  --non-interactive --agree-tos -m medusadbt@gmail.com

sudo openssl dhparam -out /etc/ssl/certs/dhparam.pem 2048

sudo systemctl enable certbot.timer
sudo certbot renew --dry-run

# kill all port runing
sudo lsof -t -iTCP:5000 -sTCP:LISTEN | xargs sudo kill

# Testing
source venv/bin/activate
python main.py
flask run --host=0.0.0.0 --port=5000
<!-- if not working, set a development override -->
export FLASK_APP=main:app
export FLASK_ENV=development
source venv/bin/activate
flask run --host=0.0.0.0 --port=5000

# Dockers
<!-- Docker -->
docker --version
docker-compose --version

sudo systemctl restart docker
sudo systemctl status docker

<!-- Start Odoo -->
<!-- locally -->
docker ps
docker-compose -f docker-compose-dev.yml down --volumes --remove-orphans
docker-compose -f system prune -a --volumes
docker-compose -f docker-compose-dev.yml down
docker-compose -f docker-compose-dev.yml up -d --build

docker-compose -f docker-compose-dev.yml down
docker-compose -f docker-compose-dev.yml up -d
docker-compose -f docker-compose-dev.yml logs -f
<!-- production -->
docker-compose -f docker-compose-prod.yml down
docker-compose -f docker-compose-prod.yml up -d
docker-compose -f docker-compose-prod.yml logs -f

# Find Your Computer's Local IP Address
ifconfig | grep inet
