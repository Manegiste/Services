sudo cp sense_status.service /etc/systemd/system
sudo cp sense_status_ip.py /usr/local/bin
sudo chmod +x /usr/local/bin/sense_status_ip.py 
sudo pip3 install netifaces
sudo pip3 install psutil
