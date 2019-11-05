Vagrant.require_version ">= 1.7.0"

$script_ctfserver = <<-SCRIPT
sudo chmod 0600 /vagrant/sshkey/id_rsa_ctf
SCRIPT

$script_controller = <<-SCRIPT
sudo ansible-galaxy install -r /vagrant/requirements.yml --force
sudo chmod o-w /vagrant/ansible
sudo chmod o-w /vagrant
SCRIPT


def import_ctfdev_config
    require 'yaml'
    current_dir    = File.dirname(File.expand_path(__FILE__))

    begin
        YAML.load_file("#{current_dir}/vagrant_ctfdev_config.local.yml")
    rescue
        YAML.load_file("#{current_dir}/vagrant_ctfdev_config.yml")
    end
end

ctfdev_config = import_ctfdev_config

Vagrant.configure("2") do |config|
    if ctfdev_config['provider'] == 'libvirt'
        config.vm.provider "libvirt"
    else
        config.vm.provider "virtualbox"
    end

    config.vm.box = "generic/ubuntu1604"

    config.vm.define "ctfserver" do |machine|
        machine.vm.hostname = "ctfserver"
        machine.vm.network "private_network", ip: "172.16.17.10"
        if ctfdev_config['provider'] == 'libvirt'

            machine.vm.provider :libvirt do |lv|
                lv.machine_virtual_size = ctfdev_config['ctfserver_disk']
                lv.memory = ctfdev_config['ctfserver_ram']
                lv.cpus = ctfdev_config['ctfserver_cpu']

                machine.vm.synced_folder './', '/vagrant', type: 'nfs'
            end
        elsif ctfdev_config['provider'] == 'virtualbox'
            unless Vagrant.has_plugin?("vagrant-disksize")
                raise 'vagrant-disksize is not installed!'
            end
            machine.vm.provider :virtualbox do |vb|
                vb.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]

                config.disksize.size = '%dGB' % [ctfdev_config['ctfserver_disk']]
                vb.memory = ctfdev_config['ctfserver_ram']
                vb.cpus = ctfdev_config['ctfserver_cpu']
                vb.customize ["modifyvm", :id, "--audio", "none"]
                machine.vm.synced_folder ".", "/vagrant"
            end
        end

        machine.vm.provision "shell", inline: $script_ctfserver
    end
    

    ctf_ansi_provision = lambda do |cf, playbook, provider|
        config.vm.provision "ansible_local" do |ansible|
              ansible.playbook       = "#{playbook}"
              ansible.config_file = "ansible/ansible.cfg"
              ansible.verbose        = true
              ansible.limit          = "all"
              ansible.inventory_path = "inventories/vagrant_#{provider}"
              ansible.verbose        = ""
        end
    end

    config.vm.define 'controller' do |machine|
        machine.vm.hostname = "controller"
        machine.vm.network "private_network", ip: "172.16.17.5"


        if ctfdev_config['provider'] == 'libvirt'
            machine.vm.provider :libvirt do |lv, override|
                lv.memory = 1024
                lv.cpus = 1
                machine.vm.synced_folder './', '/vagrant', type: 'nfs'
                machine.vm.provision "shell", inline: $script_controller
                ctf_ansi_provision.call(override, "site.yml", "libvirt")
            end

        elsif ctfdev_config['provider'] == 'virtualbox'
            machine.vm.provider :virtualbox do |vb, override|
                vb.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]

                vb.memory = 1024
                vb.cpus = 1
                vb.customize ["modifyvm", :id, "--audio", "none"]
                machine.vm.synced_folder ".", "/vagrant"
                machine.vm.provision "shell", inline: $script_controller
                ctf_ansi_provision.call(override, "site.yml", "virtualbox")
            end
        end

    end
end

