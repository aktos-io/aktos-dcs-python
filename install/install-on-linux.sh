#!/bin/bash 
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

if [[ $(id -u) > 0 ]]; then 
	echo "this tool needs root privileges"
	f="$DIR/$(basename $0)"
	echo "$f"
        sudo $f
        exit
fi

apt-get update
if ! hash pip; then
	echo "python-pip is needed..."
	apt-get install -y python-pip
fi 
apt-get install -y python-dev 
apt-get install -y libmysqlclient-dev
apt-get install -y python-zmq
apt-get install -y libpgm-5.1-0
apt-get install -y libzmq3-dev || { 
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

#pip install -U -r requirements.txt
while read p; do
    echo "Installing $p via easy_install"
    sudo easy_install -U $p
done < requirements.txt

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "Adding aktos_dcs in Python Path..."
PYTHON_MODULES="/usr/lib/python2.7/dist-packages"
sudo ln -sf "$DIR/aktos_dcs" $PYTHON_MODULES

echo "Adding update-aktos-dcs script in path..."
sudo ln -sf "$DIR/update-aktos-dcs" /usr/bin
chmod +x "$DIR/update-aktos-dcs"



