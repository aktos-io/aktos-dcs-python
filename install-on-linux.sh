#!/bin/bash 

if [[ $(id -u) > 0 ]]; then 
	echo "this tool needs root privileges"
        sudo $0
        exit
fi

if ! hash pip; then
	echo "python-pip is needed..."
	apt-get update
	apt-get install -y python-pip
fi 
apt-get install python-dev 
apt-get install libzmq3-dev || { 
	echo; 
	echo "ERROR: libzmq 4.x is needed!"
	echo; 
	echo "Install by yourself (from source) or install precompiled package"; 
	echo; 
	echo "Note: For RaspberryPi: "; 
	echo "     "; 
	echo "      https://github.com/ceremcem/libzmq-4.x-armhf-cca.git"; 
	echo; 
	echo "After installation, press enter to continue..."; read -p "Press Enter to continue";
	 }
pip install -r requirements.txt
