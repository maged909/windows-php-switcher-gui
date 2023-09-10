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

		git clone https://github.com/maged909/windows-php-switcher.git
		
	or download it you can also look up the [Releases](https://github.com/maged909/windows-php-switcher/releases) :)

-	change the current directory to windows-php-switcher-gui

		cd windows-php-switcher
		
-	install python requirements

		pip install -r requirements.txt

# Requirements
only if you're using .py file:

	customtkinter==5.2.0
	tabulate==0.9.0
	ttkthemes==3.2.2

# Configration
Go to config.js and add the php versions you want with their absolute path
here's an example

	{
    "php7.3": {
        "path": "C:\\xampp\\php"
    },
    "php8.2.3": {
        "path": "C:\\xampp\\php823"
    }
	}
	
here i have two php versions php7.3 and php8.2.3 each one with their selection that would show in menu and their path that would be used in the environment variable
i'm here using php in my xampp folder but you can point to wherever you have the php 

# Config Notes
- each php version must have selection and path
- selection must be unique for each php version
- path must be a valid absolute path to the php folder not file and cannot contain ";"
	
	
# Usage
to use it just run the phpSwitcher.py on a terminal that has an adminstrator permissions

	python phpSwitcher.py

or you can simply double click the phpSwitcher.py file Or the .exe file
	
- keep in mind that the program would ask for primission that's just coz it needs that to modify the system environment variable "PATH"
- after changing the php any already opened terminals would still be working with the old php so you need to restart them

# Console App
also you can check the console app version of php-switcher here https://github.com/maged909/windows-php-switcher/tree/main


