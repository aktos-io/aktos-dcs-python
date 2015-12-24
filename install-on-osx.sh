#!/bin/bash 

if [[ $(id -u) > 0 ]]; then 
	echo "this tool needs root privileges"
        sudo $0
        exit
fi

brew update

# pip comes out of box for Os X since 10.6.
# But any dev using homebrew's python instead of Osx provided,
# has to run `sudo easy_install pip` after installing python,
# Again it won't be an issue because for most of the devs who switches to homebrew python,
# most likely do this for new pip.
# python-dev also comes default with Os X.

#if ! hash pip; then
#	echo "python-pip is needed..."
#	apt-get install -y python-pip
#fi

# zeromq is a bottled package comes along with headers & sources linux counterpart as libzmq*-dev
brew install libpgm
brew install zeromq || {
	echo; 
	echo "ERROR: pyzmq 4.x is needed!"
	echo; 
	echo "Install by yourself (from source) or install precompiled package"; 
	echo; 
	echo "Note: For RaspberryPi: "; 
	echo "     "; 
	echo "      https://github.com/ceremcem/libzmq-4.x-armhf-cca.git"; 
	echo; 
	echo "After installation, press enter to continue..."; read -p "Press Enter to continue";
	 }
pip install -U -r requirements.txt
