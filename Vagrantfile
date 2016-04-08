# -*- mode: ruby -*-
# vi: set ft=ruby :

##########################################
#                                        #
# Provisions an ubuntu/trusty64 box with #
# 1GB of RAM, then executes bootstrap.sh #
# to provision VM.                       #
##########################################

Vagrant.configure(2) do |config|
  config.vm.box = "ubuntu/trusty64"
  config.vm.provider "virtualbox" do |vb|
    vb.memory = "1024"
   end
  config.vm.provision :shell, path: "bootstrap.sh"
end
