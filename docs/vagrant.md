# Installation of Vagrant and Dependencies

1. Install Vagrant from https://www.vagrantup.com/downloads.html


Successfully tested with Vagrant 2.2.4 (2.2.5 not working)

# vagrant-libvirt

Plugin is used for libvirt support for Vagrant

1. Install ruby-dev from apt or similar
1. run: `vagrant plugin install vagrant-libvirt`
1. if something fails, read https://github.com/vagrant-libvirt/vagrant-libvirt#possible-problems-with-plugin-installation-on-linux for any problems arising

# vagrant-disksize

Plugin is used to expand the disk used by the development VM in VirtualBox

1. run: `vagrant plugin install vagrant-disksize`
