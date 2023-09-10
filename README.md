<h1><span align="center">
  <img src="https://raw.githubusercontent.com/maged909/windows-php-switcher-gui/main/phpswitcher.ico" alt="Icon" width="40" height="40">
</span>
PHP Switcher GUI</h1>
php switcher is a simple tool created with python to help manage and switch between multiple php versions by simply changing the PATH variable to tell windows at where the desired php version is located.


![program picture](https://github.com/maged909/windows-php-switcher-gui/blob/main/phpSwitcherGUI.jpg)
![program picture](https://github.com/maged909/windows-php-switcher-gui/blob/main/phpSwitcherGUI-edit-tab.jpg)

- [Installation](#installation)
- [Requirements](#requirements)
- [Configration](#configration)
- [Config Notes](#config-notes)
- [Usage](#usage)
- [Console App](#console-app)


# Installation
only if you're using .py file:
-	clone the repo

		git clone https://github.com/maged909/windows-php-switcher-gui.git
		

-	change the current directory to windows-php-switcher-gui

		cd windows-php-switcher-gui
		
-	install python requirements

		pip install -r requirements.txt

or check out the [Releases](https://github.com/maged909/windows-php-switcher-gui/releases) :)

# Requirements
only if you're using .py file:

	customtkinter==5.2.0
	tabulate==0.9.0
	ttkthemes==3.2.2

# Configration
config.js will contain the information about the available php versions and it would look something like that, you wouldn't need to edit the file directly as the app have an "Edit Config" tab

	{
    "php7.3": {
        "path": "C:\\xampp\\php"
    },
    "php8.2.3": {
        "path": "C:\\xampp\\php823"
    }
	}

# Config Notes
- each php version must have path
- path and name must be unique for each php version
- path must be a valid absolute path to the php folder not file and cannot contain ";"
	
	
# Usage
to use it just run the phpSwitcher.py on a terminal that has an adminstrator permissions

	python phpSwitcherGui.py

or you can simply double click the phpSwitcherGui.py file Or the .exe file
	
- keep in mind that the program would ask for primission that's just coz it needs that to modify the system environment variable "PATH"
- after changing the php any already opened terminals would still be working with the old php so you need to restart them

# Console App
also you can check the console app version of php-switcher here https://github.com/maged909/windows-php-switcher-gui


