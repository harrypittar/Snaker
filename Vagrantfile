# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|

  config.vm.define "gameserver" do |gs|
    gs.vm.box = "gusztavvargadr/ubuntu-desktop"
    gs.vm.hostname = "gameserver"
    gs.vm.network "private_network", ip: "192.168.2.11"
    gs.vm.synced_folder "shared", "/vagrant", owner: "vagrant", group: "vagrant", mount_options: ["dmode=775,fmode=777"]

    gs.vm.provider "virtualbox" do |vb|
      # Display the VirtualBox GUI when booting the machine
      vb.gui = true

      # Customize the amount of memory on the VM:
      vb.memory = "1024"
    end

    gs.vm.provision "shell", inline: <<-SHELL
      chmod +x /vagrant/build-gameserver-vm.sh
      yes | /vagrant/build-gameserver-vm.sh
    SHELL
  end

  config.vm.define "dbserver" do |dbs|
    dbs.vm.box = "ubuntu/xenial64"
    dbs.vm.hostname = "dbserver"
    dbs.vm.network "private_network", ip: "192.168.2.12"
    dbs.vm.synced_folder "shared", "/vagrant", owner: "vagrant", group: "vagrant", mount_options: ["dmode=775,fmode=777"]

    dbs.vm.provision "shell", inline: <<-SHELL
      sh /vagrant/build-dbserver-vm.sh
    SHELL
  end

  config.vm.define "webserver" do |ws|
    ws.vm.box = "ubuntu/xenial64"
    ws.vm.hostname = "webserver"
    ws.vm.network "forwarded_port", guest: 80, host: 8080, host_ip: "127.0.0.1"
    ws.vm.network "private_network", ip: "192.168.2.13"
    ws.vm.synced_folder "shared", "/vagrant", owner: "vagrant", group: "vagrant", mount_options: ["dmode=775,fmode=777"]

    ws.vm.provision "shell", inline: <<-SHELL
      sh /vagrant/build-webserver-vm.sh
    SHELL
  end

end
