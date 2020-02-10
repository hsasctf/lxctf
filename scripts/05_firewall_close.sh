
#!/bin/bash

sudo iptables -D FORWARD 1 -s 10.40.1.0/24 -d 10.40.2.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.1.0/24 -d 10.40.2.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.1.0/24 -d 10.40.2.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.1.0/24 -d 10.40.2.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.41.1.0/24 -d 10.40.2.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.1.0/24 -d 10.40.2.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.1.0/24 -d 10.40.2.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.1.0/24 -d 10.40.2.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.42.1.0/24 -d 10.40.2.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.1.0/24 -d 10.40.2.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.1.0/24 -d 10.40.2.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.1.0/24 -d 10.40.2.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.40.1.0/24 -d 10.40.3.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.1.0/24 -d 10.40.3.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.1.0/24 -d 10.40.3.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.1.0/24 -d 10.40.3.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.41.1.0/24 -d 10.40.3.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.1.0/24 -d 10.40.3.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.1.0/24 -d 10.40.3.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.1.0/24 -d 10.40.3.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.42.1.0/24 -d 10.40.3.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.1.0/24 -d 10.40.3.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.1.0/24 -d 10.40.3.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.1.0/24 -d 10.40.3.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.40.1.0/24 -d 10.40.4.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.1.0/24 -d 10.40.4.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.1.0/24 -d 10.40.4.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.1.0/24 -d 10.40.4.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.41.1.0/24 -d 10.40.4.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.1.0/24 -d 10.40.4.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.1.0/24 -d 10.40.4.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.1.0/24 -d 10.40.4.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.42.1.0/24 -d 10.40.4.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.1.0/24 -d 10.40.4.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.1.0/24 -d 10.40.4.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.1.0/24 -d 10.40.4.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.40.1.0/24 -d 10.40.5.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.1.0/24 -d 10.40.5.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.1.0/24 -d 10.40.5.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.1.0/24 -d 10.40.5.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.41.1.0/24 -d 10.40.5.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.1.0/24 -d 10.40.5.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.1.0/24 -d 10.40.5.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.1.0/24 -d 10.40.5.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.42.1.0/24 -d 10.40.5.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.1.0/24 -d 10.40.5.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.1.0/24 -d 10.40.5.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.1.0/24 -d 10.40.5.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.40.1.0/24 -d 10.40.6.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.1.0/24 -d 10.40.6.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.1.0/24 -d 10.40.6.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.1.0/24 -d 10.40.6.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.41.1.0/24 -d 10.40.6.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.1.0/24 -d 10.40.6.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.1.0/24 -d 10.40.6.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.1.0/24 -d 10.40.6.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.42.1.0/24 -d 10.40.6.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.1.0/24 -d 10.40.6.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.1.0/24 -d 10.40.6.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.1.0/24 -d 10.40.6.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.40.1.0/24 -d 10.40.7.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.1.0/24 -d 10.40.7.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.1.0/24 -d 10.40.7.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.1.0/24 -d 10.40.7.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.41.1.0/24 -d 10.40.7.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.1.0/24 -d 10.40.7.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.1.0/24 -d 10.40.7.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.1.0/24 -d 10.40.7.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.42.1.0/24 -d 10.40.7.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.1.0/24 -d 10.40.7.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.1.0/24 -d 10.40.7.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.1.0/24 -d 10.40.7.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.40.2.0/24 -d 10.40.1.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.2.0/24 -d 10.40.1.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.2.0/24 -d 10.40.1.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.2.0/24 -d 10.40.1.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.41.2.0/24 -d 10.40.1.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.2.0/24 -d 10.40.1.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.2.0/24 -d 10.40.1.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.2.0/24 -d 10.40.1.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.42.2.0/24 -d 10.40.1.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.2.0/24 -d 10.40.1.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.2.0/24 -d 10.40.1.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.2.0/24 -d 10.40.1.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.40.2.0/24 -d 10.40.3.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.2.0/24 -d 10.40.3.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.2.0/24 -d 10.40.3.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.2.0/24 -d 10.40.3.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.41.2.20/24 -d 10.40.3.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.2.20/24 -d 10.40.3.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.2.20/24 -d 10.40.3.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.2.20/24 -d 10.40.3.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.42.2.0/24 -d 10.40.3.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.2.0/24 -d 10.40.3.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.2.0/24 -d 10.40.3.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.2.0/24 -d 10.40.3.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.40.2.0/24 -d 10.40.4.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.2.0/24 -d 10.40.4.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.2.0/24 -d 10.40.4.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.2.0/24 -d 10.40.4.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.41.2.0/24 -d 10.40.4.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.2.0/24 -d 10.40.4.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.2.0/24 -d 10.40.4.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.2.0/24 -d 10.40.4.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.42.2.0/24 -d 10.40.4.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.2.0/24 -d 10.40.4.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.2.0/24 -d 10.40.4.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.2.0/24 -d 10.40.4.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.40.2.0/24 -d 10.40.5.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.2.0/24 -d 10.40.5.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.2.0/24 -d 10.40.5.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.2.0/24 -d 10.40.5.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.41.2.0/24 -d 10.40.5.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.2.0/24 -d 10.40.5.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.2.0/24 -d 10.40.5.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.2.0/24 -d 10.40.5.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.42.2.0/24 -d 10.40.5.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.2.0/24 -d 10.40.5.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.2.0/24 -d 10.40.5.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.2.0/24 -d 10.40.5.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.40.2.0/24 -d 10.40.6.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.2.0/24 -d 10.40.6.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.2.0/24 -d 10.40.6.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.2.0/24 -d 10.40.6.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.41.2.0/24 -d 10.40.6.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.2.0/24 -d 10.40.6.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.2.0/24 -d 10.40.6.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.2.0/24 -d 10.40.6.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.42.2.0/24 -d 10.40.6.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.2.0/24 -d 10.40.6.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.2.0/24 -d 10.40.6.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.2.0/24 -d 10.40.6.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.40.2.0/24 -d 10.40.7.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.2.0/24 -d 10.40.7.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.2.0/24 -d 10.40.7.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.2.0/24 -d 10.40.7.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.41.2.0/24 -d 10.40.7.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.2.0/24 -d 10.40.7.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.2.0/24 -d 10.40.7.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.2.0/24 -d 10.40.7.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.42.2.0/24 -d 10.40.7.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.2.0/24 -d 10.40.7.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.2.0/24 -d 10.40.7.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.2.0/24 -d 10.40.7.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.40.3.0/24 -d 10.40.1.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.3.0/24 -d 10.40.1.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.3.0/24 -d 10.40.1.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.3.0/24 -d 10.40.1.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.41.3.0/24 -d 10.40.1.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.3.0/24 -d 10.40.1.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.3.0/24 -d 10.40.1.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.3.0/24 -d 10.40.1.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.42.3.0/24 -d 10.40.1.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.3.0/24 -d 10.40.1.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.3.0/24 -d 10.40.1.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.3.0/24 -d 10.40.1.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.40.3.0/24 -d 10.40.2.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.3.0/24 -d 10.40.2.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.3.0/24 -d 10.40.2.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.3.0/24 -d 10.40.2.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.41.3.20/24 -d 10.40.2.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.3.20/24 -d 10.40.2.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.3.20/24 -d 10.40.2.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.3.20/24 -d 10.40.2.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.42.3.0/24 -d 10.40.2.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.3.0/24 -d 10.40.2.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.3.0/24 -d 10.40.2.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.3.0/24 -d 10.40.2.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.40.3.0/24 -d 10.40.4.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.3.0/24 -d 10.40.4.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.3.0/24 -d 10.40.4.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.3.0/24 -d 10.40.4.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.41.3.0/24 -d 10.40.4.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.3.0/24 -d 10.40.4.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.3.0/24 -d 10.40.4.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.3.0/24 -d 10.40.4.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.42.3.0/24 -d 10.40.4.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.3.0/24 -d 10.40.4.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.3.0/24 -d 10.40.4.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.3.0/24 -d 10.40.4.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.40.3.0/24 -d 10.40.5.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.3.0/24 -d 10.40.5.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.3.0/24 -d 10.40.5.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.3.0/24 -d 10.40.5.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.41.3.0/24 -d 10.40.5.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.3.0/24 -d 10.40.5.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.3.0/24 -d 10.40.5.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.3.0/24 -d 10.40.5.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.42.3.0/24 -d 10.40.5.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.3.0/24 -d 10.40.5.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.3.0/24 -d 10.40.5.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.3.0/24 -d 10.40.5.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.40.3.0/24 -d 10.40.6.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.3.0/24 -d 10.40.6.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.3.0/24 -d 10.40.6.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.3.0/24 -d 10.40.6.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.41.3.0/24 -d 10.40.6.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.3.0/24 -d 10.40.6.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.3.0/24 -d 10.40.6.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.3.0/24 -d 10.40.6.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.42.3.0/24 -d 10.40.6.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.3.0/24 -d 10.40.6.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.3.0/24 -d 10.40.6.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.3.0/24 -d 10.40.6.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.40.3.0/24 -d 10.40.7.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.3.0/24 -d 10.40.7.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.3.0/24 -d 10.40.7.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.3.0/24 -d 10.40.7.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.41.3.0/24 -d 10.40.7.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.3.0/24 -d 10.40.7.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.3.0/24 -d 10.40.7.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.3.0/24 -d 10.40.7.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.42.3.0/24 -d 10.40.7.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.3.0/24 -d 10.40.7.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.3.0/24 -d 10.40.7.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.3.0/24 -d 10.40.7.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.40.4.0/24 -d 10.40.1.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.4.0/24 -d 10.40.1.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.4.0/24 -d 10.40.1.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.4.0/24 -d 10.40.1.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.41.4.0/24 -d 10.40.1.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.4.0/24 -d 10.40.1.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.4.0/24 -d 10.40.1.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.4.0/24 -d 10.40.1.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.42.4.0/24 -d 10.40.1.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.4.0/24 -d 10.40.1.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.4.0/24 -d 10.40.1.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.4.0/24 -d 10.40.1.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.40.4.0/24 -d 10.40.2.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.4.0/24 -d 10.40.2.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.4.0/24 -d 10.40.2.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.4.0/24 -d 10.40.2.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.41.4.20/24 -d 10.40.2.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.4.20/24 -d 10.40.2.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.4.20/24 -d 10.40.2.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.4.20/24 -d 10.40.2.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.42.4.0/24 -d 10.40.2.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.4.0/24 -d 10.40.2.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.4.0/24 -d 10.40.2.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.4.0/24 -d 10.40.2.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.40.4.0/24 -d 10.40.3.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.4.0/24 -d 10.40.3.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.4.0/24 -d 10.40.3.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.4.0/24 -d 10.40.3.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.41.4.0/24 -d 10.40.3.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.4.0/24 -d 10.40.3.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.4.0/24 -d 10.40.3.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.4.0/24 -d 10.40.3.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.42.4.0/24 -d 10.40.3.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.4.0/24 -d 10.40.3.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.4.0/24 -d 10.40.3.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.4.0/24 -d 10.40.3.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.40.4.0/24 -d 10.40.5.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.4.0/24 -d 10.40.5.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.4.0/24 -d 10.40.5.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.4.0/24 -d 10.40.5.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.41.4.0/24 -d 10.40.5.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.4.0/24 -d 10.40.5.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.4.0/24 -d 10.40.5.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.4.0/24 -d 10.40.5.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.42.4.0/24 -d 10.40.5.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.4.0/24 -d 10.40.5.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.4.0/24 -d 10.40.5.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.4.0/24 -d 10.40.5.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.40.4.0/24 -d 10.40.6.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.4.0/24 -d 10.40.6.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.4.0/24 -d 10.40.6.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.4.0/24 -d 10.40.6.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.41.4.0/24 -d 10.40.6.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.4.0/24 -d 10.40.6.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.4.0/24 -d 10.40.6.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.4.0/24 -d 10.40.6.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.42.4.0/24 -d 10.40.6.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.4.0/24 -d 10.40.6.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.4.0/24 -d 10.40.6.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.4.0/24 -d 10.40.6.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.40.4.0/24 -d 10.40.7.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.4.0/24 -d 10.40.7.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.4.0/24 -d 10.40.7.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.4.0/24 -d 10.40.7.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.41.4.0/24 -d 10.40.7.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.4.0/24 -d 10.40.7.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.4.0/24 -d 10.40.7.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.4.0/24 -d 10.40.7.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.42.4.0/24 -d 10.40.7.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.4.0/24 -d 10.40.7.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.4.0/24 -d 10.40.7.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.4.0/24 -d 10.40.7.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.40.5.0/24 -d 10.40.1.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.5.0/24 -d 10.40.1.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.5.0/24 -d 10.40.1.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.5.0/24 -d 10.40.1.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.41.5.0/24 -d 10.40.1.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.5.0/24 -d 10.40.1.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.5.0/24 -d 10.40.1.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.5.0/24 -d 10.40.1.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.42.5.0/24 -d 10.40.1.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.5.0/24 -d 10.40.1.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.5.0/24 -d 10.40.1.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.5.0/24 -d 10.40.1.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.40.5.0/24 -d 10.40.2.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.5.0/24 -d 10.40.2.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.5.0/24 -d 10.40.2.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.5.0/24 -d 10.40.2.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.41.5.20/24 -d 10.40.2.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.5.20/24 -d 10.40.2.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.5.20/24 -d 10.40.2.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.5.20/24 -d 10.40.2.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.42.5.0/24 -d 10.40.2.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.5.0/24 -d 10.40.2.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.5.0/24 -d 10.40.2.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.5.0/24 -d 10.40.2.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.40.5.0/24 -d 10.40.3.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.5.0/24 -d 10.40.3.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.5.0/24 -d 10.40.3.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.5.0/24 -d 10.40.3.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.41.5.0/24 -d 10.40.3.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.5.0/24 -d 10.40.3.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.5.0/24 -d 10.40.3.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.5.0/24 -d 10.40.3.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.42.5.0/24 -d 10.40.3.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.5.0/24 -d 10.40.3.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.5.0/24 -d 10.40.3.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.5.0/24 -d 10.40.3.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.40.5.0/24 -d 10.40.4.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.5.0/24 -d 10.40.4.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.5.0/24 -d 10.40.4.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.5.0/24 -d 10.40.4.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.41.5.0/24 -d 10.40.4.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.5.0/24 -d 10.40.4.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.5.0/24 -d 10.40.4.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.5.0/24 -d 10.40.4.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.42.5.0/24 -d 10.40.4.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.5.0/24 -d 10.40.4.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.5.0/24 -d 10.40.4.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.5.0/24 -d 10.40.4.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.40.5.0/24 -d 10.40.6.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.5.0/24 -d 10.40.6.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.5.0/24 -d 10.40.6.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.5.0/24 -d 10.40.6.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.41.5.0/24 -d 10.40.6.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.5.0/24 -d 10.40.6.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.5.0/24 -d 10.40.6.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.5.0/24 -d 10.40.6.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.42.5.0/24 -d 10.40.6.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.5.0/24 -d 10.40.6.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.5.0/24 -d 10.40.6.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.5.0/24 -d 10.40.6.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.40.5.0/24 -d 10.40.7.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.5.0/24 -d 10.40.7.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.5.0/24 -d 10.40.7.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.5.0/24 -d 10.40.7.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.41.5.0/24 -d 10.40.7.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.5.0/24 -d 10.40.7.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.5.0/24 -d 10.40.7.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.5.0/24 -d 10.40.7.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.42.5.0/24 -d 10.40.7.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.5.0/24 -d 10.40.7.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.5.0/24 -d 10.40.7.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.5.0/24 -d 10.40.7.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.40.6.0/24 -d 10.40.1.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.6.0/24 -d 10.40.1.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.6.0/24 -d 10.40.1.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.6.0/24 -d 10.40.1.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.41.6.0/24 -d 10.40.1.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.6.0/24 -d 10.40.1.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.6.0/24 -d 10.40.1.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.6.0/24 -d 10.40.1.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.42.6.0/24 -d 10.40.1.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.6.0/24 -d 10.40.1.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.6.0/24 -d 10.40.1.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.6.0/24 -d 10.40.1.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.40.6.0/24 -d 10.40.2.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.6.0/24 -d 10.40.2.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.6.0/24 -d 10.40.2.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.6.0/24 -d 10.40.2.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.41.6.20/24 -d 10.40.2.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.6.20/24 -d 10.40.2.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.6.20/24 -d 10.40.2.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.6.20/24 -d 10.40.2.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.42.6.0/24 -d 10.40.2.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.6.0/24 -d 10.40.2.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.6.0/24 -d 10.40.2.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.6.0/24 -d 10.40.2.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.40.6.0/24 -d 10.40.3.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.6.0/24 -d 10.40.3.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.6.0/24 -d 10.40.3.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.6.0/24 -d 10.40.3.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.41.6.0/24 -d 10.40.3.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.6.0/24 -d 10.40.3.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.6.0/24 -d 10.40.3.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.6.0/24 -d 10.40.3.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.42.6.0/24 -d 10.40.3.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.6.0/24 -d 10.40.3.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.6.0/24 -d 10.40.3.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.6.0/24 -d 10.40.3.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.40.6.0/24 -d 10.40.4.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.6.0/24 -d 10.40.4.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.6.0/24 -d 10.40.4.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.6.0/24 -d 10.40.4.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.41.6.0/24 -d 10.40.4.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.6.0/24 -d 10.40.4.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.6.0/24 -d 10.40.4.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.6.0/24 -d 10.40.4.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.42.6.0/24 -d 10.40.4.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.6.0/24 -d 10.40.4.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.6.0/24 -d 10.40.4.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.6.0/24 -d 10.40.4.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.40.6.0/24 -d 10.40.5.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.6.0/24 -d 10.40.5.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.6.0/24 -d 10.40.5.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.6.0/24 -d 10.40.5.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.41.6.0/24 -d 10.40.5.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.6.0/24 -d 10.40.5.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.6.0/24 -d 10.40.5.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.6.0/24 -d 10.40.5.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.42.6.0/24 -d 10.40.5.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.6.0/24 -d 10.40.5.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.6.0/24 -d 10.40.5.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.6.0/24 -d 10.40.5.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.40.6.0/24 -d 10.40.7.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.6.0/24 -d 10.40.7.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.6.0/24 -d 10.40.7.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.6.0/24 -d 10.40.7.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.41.6.0/24 -d 10.40.7.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.6.0/24 -d 10.40.7.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.6.0/24 -d 10.40.7.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.6.0/24 -d 10.40.7.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.42.6.0/24 -d 10.40.7.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.6.0/24 -d 10.40.7.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.6.0/24 -d 10.40.7.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.6.0/24 -d 10.40.7.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.7.0/24 -d 10.40.1.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.7.0/24 -d 10.40.1.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.7.0/24 -d 10.40.1.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.7.0/24 -d 10.40.1.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.41.7.0/24 -d 10.40.1.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.7.0/24 -d 10.40.1.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.7.0/24 -d 10.40.1.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.7.0/24 -d 10.40.1.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.42.7.0/24 -d 10.40.1.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.7.0/24 -d 10.40.1.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.7.0/24 -d 10.40.1.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.7.0/24 -d 10.40.1.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.40.7.0/24 -d 10.40.2.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.7.0/24 -d 10.40.2.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.7.0/24 -d 10.40.2.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.7.0/24 -d 10.40.2.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.41.7.20/24 -d 10.40.2.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.7.20/24 -d 10.40.2.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.7.20/24 -d 10.40.2.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.7.20/24 -d 10.40.2.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.42.7.0/24 -d 10.40.2.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.7.0/24 -d 10.40.2.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.7.0/24 -d 10.40.2.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.7.0/24 -d 10.40.2.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.40.7.0/24 -d 10.40.3.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.7.0/24 -d 10.40.3.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.7.0/24 -d 10.40.3.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.7.0/24 -d 10.40.3.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.41.7.0/24 -d 10.40.3.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.7.0/24 -d 10.40.3.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.7.0/24 -d 10.40.3.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.7.0/24 -d 10.40.3.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.42.7.0/24 -d 10.40.3.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.7.0/24 -d 10.40.3.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.7.0/24 -d 10.40.3.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.7.0/24 -d 10.40.3.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.40.7.0/24 -d 10.40.4.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.7.0/24 -d 10.40.4.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.7.0/24 -d 10.40.4.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.7.0/24 -d 10.40.4.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.41.7.0/24 -d 10.40.4.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.7.0/24 -d 10.40.4.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.7.0/24 -d 10.40.4.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.7.0/24 -d 10.40.4.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.42.7.0/24 -d 10.40.4.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.7.0/24 -d 10.40.4.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.7.0/24 -d 10.40.4.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.7.0/24 -d 10.40.4.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.40.7.0/24 -d 10.40.5.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.7.0/24 -d 10.40.5.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.7.0/24 -d 10.40.5.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.7.0/24 -d 10.40.5.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.41.7.0/24 -d 10.40.5.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.7.0/24 -d 10.40.5.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.7.0/24 -d 10.40.5.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.7.0/24 -d 10.40.5.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.42.7.0/24 -d 10.40.5.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.7.0/24 -d 10.40.5.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.7.0/24 -d 10.40.5.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.7.0/24 -d 10.40.5.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.40.7.0/24 -d 10.40.6.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.7.0/24 -d 10.40.6.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.7.0/24 -d 10.40.6.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.40.7.0/24 -d 10.40.6.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.41.7.0/24 -d 10.40.6.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.7.0/24 -d 10.40.6.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.7.0/24 -d 10.40.6.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.41.7.0/24 -d 10.40.6.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT

sudo iptables -D FORWARD 1 -s 10.42.7.0/24 -d 10.40.6.0/24 -p tcp -m tcp --dport 5101 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.7.0/24 -d 10.40.6.0/24 -p tcp -m tcp --dport 5102 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.7.0/24 -d 10.40.6.0/24 -p tcp -m tcp --dport 5103 -j ACCEPT
sudo iptables -D FORWARD 1 -s 10.42.7.0/24 -d 10.40.6.0/24 -p tcp -m tcp --dport 5104 -j ACCEPT
