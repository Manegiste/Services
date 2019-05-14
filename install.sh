sudo cp lcdip.service /etc/systemd/system
sudo cp shtdwn.service /etc/systemd/system
sudo cp LCDIP.py /usr/local/bin
sudo cp SHTDWN.py /usr/local/bin
sudo chmod +x /usr/local/bin/LCDIP.py 
sudo chmod +x /usr/local/bin/SHTDWN.py 
sudo pip install netifaces
sudo pip install psutil
