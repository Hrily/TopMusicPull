#!/bin/bash

#First update the given System
sudo apt-get update > install_verbose.txt
>> install_verbose.txt
#Install Python pip to install Python based dependencies
sudo sudo apt-get inst >> install_verbose.txtall python-pip >> install_verbose.txt

 >> install_verbose.txt
#Refresh to update
sudo apt-get update >>  install_verbose.txt
#Install the youtube-dl dependency
sudo pip install youtube-dl >> install_verbose.txt
#Install Python Installer
sudo pip install PyInstaller >> install_verbose.txt
#Install mid3v2
sudo pip install mutagen >> install_verbose.txt

#Move the Binary compiled file to the bin folder
sudo cp dist/music_crawler /bin

#remove generated installation verbose file
sudo rm -rf install_verbose.txt
