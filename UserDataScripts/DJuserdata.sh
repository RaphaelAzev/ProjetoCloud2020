#!/bin/bash
sudo apt update
cd /home/ubuntu
git clone https://github.com/raulikeda/tasks.git
cd tasks
sed -i "s/'HOST': 'node1'/'HOST': '{DB_instance_ip}'/" /home/ubuntu/tasks/portfolio/settings.py 
./install.sh
sudo reboot
