#!/bin/sh
# Installs dependencies for speedbot

sudo apt-get install python-pip
sudo pip install pyspeedtest
sudo pip install twitter
mkdir logs

# use a template to create the actual config file
cp default_config.ini config.ini
