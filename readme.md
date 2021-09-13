# Snaker
Snaker is an application which uses and manages 3 servers to run a game of snake. The servers are used to play the game, store high scores, and display the high scores on a website.

# Installation and Setup
## Installation Prerequisites
Install the required programs:
* [VirtualBox](https://www.virtualbox.org/wiki/Downloads)
* [Vagrant](https://www.vagrantup.com/downloads)

## Setup
### Step 1
From your command line, clone Snaker:
```
git clone https://github.com/rammcodes/dopefolio
```
Go into the repository:
```
cd Snaker
```

### Step 2
Create and configure virtual machines (VMs) with Vagrant:
```
vagrant up
```

Vagrant should start creating the VMs. This will take a few minutes.

# Usage
When setup is completed, a VirtualBox window should appear with the VM used for playing Snaker (the *gameserver* VM). If the VirtualBox window which hosts the server is too small, you can increase the size of the window by clicking on the button shown below and increasing the scale.
![picture](https://gcdn.pbrd.co/images/uQC1QDUgPkCr.png)

Login to the VM with the password:
```
vagrant
```

The VM may take a few minutes to load. You may run into some error messages when logging in, but you can ignore them.

To play the game:
1. Open the terminal by right-clicking on the desktop in the VirtualBox window and selecting "Open Terminal Here"
2. Go in to the Snaker game directory:
    ```
    cd /vagrant/Snaker
    ```
3. Run the game:
    ```
    python Snakegame.py
    ```
4. Type in your username, and play the game using the arrow keys. High scores will be stored in the MySQL database in the *dbserver* VM

You can then view the highscores by visiting http://127.0.0.1:8080 in your web browser. This website is stored on the *webserver* VM.

# Configuration
## Vagrant
Vagrant provides an easy way to configure and manage multiple VMs. To edit configuration of the 3 servers, open the `Vagrantfile` in the repository in a text editor. For each VM, you can configure:
* The Vagrant box which the VM uses
* The hostname of the VM
* The VM's network, which can be private or public
* Forwarded port mapping, allowing access to a port on the VM from the host machine
* A shared folder between the VM and host machine
* VM provisioning, which runs Unix shell commands on the VM after it has been created
    * Shell scripts for provision each VM can be found in the `shared` folder
* and much more (see Vagrant documentation)...

Configuration for a VM may look like this:
```
# Define the database server
  config.vm.define "dbserver" do |dbs|
    dbs.vm.box = "ubuntu/xenial64"
    dbs.vm.hostname = "dbserver"
    dbs.vm.network "private_network", ip: "192.168.2.12"
    dbs.vm.synced_folder "shared", "/vagrant", owner: "vagrant", group: "vagrant", mount_options: ["dmode=775,fmode=777"]

    # Execute shell script to provision VM
    dbs.vm.provision "shell", inline: <<-SHELL
      sh /vagrant/build-dbserver-vm.sh
    SHELL
  end
```

## Snake Game
You can edit the game's source code by editing the `shared/Snaker/Snakegame.py` file. As the source code is in the /shared folder, changes made to the source code will show up immediately in the VM. This is true for all files in the `shared` folder.

## MySQL Database
Configure the database by editing the `shared/build_dbserver_vm.sh` file, and run initial MySQL queries with the `shared/setup-database.sql` file. We suggest changing the root password on `line 5` of `shared/build_dbserver_vm.sh`, and your user password on `lines 25 and 33`.

If you do change the user password, you must also edit the password on `line 221` of the game's python source code, and `line 31` of `shared/www/index.php` (the PHP file which displays high scores on a website).

## Webserver
Provisioning for the *webserver* VM can be configured by editing `shared/build_dbserver_vm.sh`. This script also activates the configuration stored in `shared/website.conf`, which you may edit.

The PHP file that displays the highscores on a web page can be found at `shared/www/index.php`. In this file, you can configure the appearance and functionality of the website. Additionally, any changes made to the database must be reflected in the PHP script section of the file.
