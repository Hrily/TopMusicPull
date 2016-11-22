#!/bin/bash

#First update the given System
sudo apt-get update
#Install Python pip to install Python based dependencies
sudo sudo apt-get install python-pip


#Refresh to update
sudo apt-get update
#Install the youtube-dl dependency
sudo pip install youtube-dl
#Install Python Installer
sudo pip install PyInstaller
#Install mid3v2
sudo pip install mutagen

#Move the Binary compiled file to the bin folder
sudo cp dist/music_crawler /bin

