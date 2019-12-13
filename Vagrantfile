Vagrant.require_version ">= 1.7.0"

$script_ctfserver = <<-SCRIPT
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
    
    ctf_ansi_provision = lambda do |playbook, inventory|
        config.vm.provision "ansible_local" do |ansible|
              ansible.playbook       = "#{playbook}"
              ansible.config_file = "ansible/ansible.cfg"
              ansible.verbose        = true
              ansible.limit          = "all"
              ansible.inventory_path = inventory
              ansible.verbose        = ""
              ansible.install_mode   = "pip"
              ansible.version        = "2.8.6"
              ansible.extra_vars = {
                  in_vagrant: true
              }
        end
    end

    config.vm.define "ctfserver" do |machine|
        machine.vm.hostname = "ctfserver"
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
      
        ctf_ansi_provision.call("vagrant_ansible.yml", "inventories/localhost")
        ctf_ansi_provision.call("site.yml", "inventories/ctf.py")

    end





end

