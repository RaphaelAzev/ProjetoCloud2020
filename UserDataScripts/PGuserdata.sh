#!/bin/bash
sudo apt update
sudo apt install postgresql postgresql-contrib -y
sudo -u postgres psql -c "CREATE USER cloud WITH PASSWORD 'cloud'; "
sudo -u postgres createdb -O cloud tasks
sed -i "s/#listen_addresses = 'localhost'/listen_addresses = '*'\t/" /etc/postgresql/10/main/postgresql.conf
echo "host    all             all             0.0.0.0/0               trust" >> /etc/postgresql/10/main/pg_hba.conf
sudo ufw allow 5432/tcp
sudo systemctl restart postgresql

