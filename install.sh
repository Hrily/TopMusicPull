#!/bin/bash

#First update the given System
sudo apt-get update
#Install Python pip to install Python based dependencies
sudo apt-get install python-pip


#Refresh to update
sudo apt-get update
#Install the youtube-dl dependency
pip install youtube-dl
#Install Python Installer
pip install PyInstaller
#Install mid3v2
pip install mutagen

#Move the Binary compiled file to the bin folder
cd dist/music_crawler
sudo cp music_crawler /bin
sudo cp libpython2.7.so.1.0 /bin

