#This file is intended to setup Vagrant VM.
# but this same file can be used to setup a physical machine such as a Rasberry pi.
# Installs python3 environment, installs requirements, updates crontab for auto-exectuion

#!/bin/bash
sudo su -
apt-get update && apt-get upgrade -y
apt-get install python-virtualenv python3-dev python3-pip -y
cd ~
pip3 install -r /vagrant/requirements.txt
# Adds a crontab to run analysis on the hour
# Cron expression
cron="0 * * * * /vagrant/app.sh "

# Escape all the asterisks so we can grep for it
cron_escaped=$(echo "$cron" | sed s/\*/\\\\*/g)

# Check if cron job already in crontab
crontab -l | grep "${cronescaped}"
if [[ $? -eq 0 ]] ;
  then
    echo "Crontab already exists. Exiting..."
    exit
  else
    # Write out current crontab into temp file
    crontab -l > mycron
    # Append new cron into cron file
    echo "$cron" >> mycron
    # Install new cron file
    crontab mycron
    # Remove temp file
    rm mycron
fi
echo "done installing"