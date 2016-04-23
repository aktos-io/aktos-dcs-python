# Install 

Compilations may take around 3 minutes. 

#### Windows: 

* install [Python 2.7.x](https://www.python.org/downloads/)
* install http://aka.ms/vcpython27
* clone repository: `git clone --recursive https://github.com/aktos-io/aktos-dcs`
* run (double click on) "`aktos-dcs\`[install-on-windows.cmd](./install-on-windows.cmd) 

> Notes for Windows
>
> First install `wheel`, then install `dep/win*/*.whl` for `MySQL-python`. 

#### Linux:

* clone repository: `git clone --recursive https://github.com/aktos-io/aktos-dcs`
* `$ cd aktos-dcs && sudo `[./install-on-linux.sh](./install-on-linux.sh) 
* Whenever you need to update, run `update-aktos-dcs` in any terminal. 

#### Os X - El Capitan:

* Requires [homebrew](http://brew.sh/) if it's not installed already. 
* clone repository: `git clone --recursive https://github.com/aktos-io/aktos-dcs`
* `$ cd aktos-dcs && `[./install-on-osx.sh](./install-on-osx.sh) 

> Notes for Mac
>
> As we don't own any Mac, updates may suffer from testing issues. 



# TODO

1. Create native scripts that will kick off installation (ie. install Python) then will run main install script. 
2. Convert all common scripts into Python scripts
3. Create a way to install everything with native single scripts: 
    
    INSTALL: 
        Windows: 
            1. download https://..../install-on-windows.cmd
            2. double-click on it. 

        Linux: 
            $ curl -s https://...../install-on-linux.sh | bash -s

        MacOSX:
            Same as Linux.   