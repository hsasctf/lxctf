# Debugging

## connect to container from controller


`ssh -o ProxyCommand="ssh -i /vagrant/.vagrant/machines/ctfserver/virtualbox/private_key -W %h:%p -q vagrant@172.16.17.10" ubuntu@10.40.1.1 -i /vagrant/sshkey/id_rsa_ctf`

