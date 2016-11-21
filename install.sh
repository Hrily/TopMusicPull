#!/bin/bash

#First update the given System
sudo apt-get update

#Install Python pip to install Python based dependencies
sudo sudo apt-get install python-pip

#Install the youtube-dl dependency
sudo pip install youtube-dl

#Refresh to update
sudo apt-get update
#Install Python Installer
sudo pip install PyInstaller
#Install mid3v2
sudo pip install mutagen

#Move the Binary compiled file to the bin folder
sudo mv dist/music_crawler /bin

