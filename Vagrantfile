# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|
  # The most common configuration options are documented and commented below.
  # For a complete reference, please see the online documentation at
  # https://docs.vagrantup.com.

  # Every Vagrant development environment requires a box. You can search for
  # boxes at https://vagrantcloud.com/search.
  config.vm.box = "ubuntu/bionic64"
  # Pin to specific version in case of changes in base image
  config.vm.box_version = "~> 20200304.0.0"
  # Maps port on local machine to port on server
  config.vm.network "forwarded_port", guest: 8000, host: 8000
  # Provision block to run scripts
  config.vm.provision "shell", inline: <<-SHELL
    # Disable auto update which conflicts with auto update below (line 27)
    # when first ran on Ubuntu
    systemctl disable apt-daily.service
    systemctl disable apt-daily.timer
    # Update line to update local repository with all available packages
    sudo apt-get update
    # Two packages python3-venv and zip
    sudo apt-get install -y python3-venv zip
    # Bash aliases file which sets Python3 to the default Python version
    # for the vagrant user
    touch /home/vagrant/.bash_aliases
    if ! grep -q PYTHON_ALIAS_ADDED /home/vagrant/.bash_aliases; then
      echo "# PYTHON_ALIAS_ADDED" >> /home/vagrant/.bash_aliases
      echo "alias python='python3'" >> /home/vagrant/.bash_aliases
    fi
  SHELL
 end
