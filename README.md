# Eyecare Reminder

Simple app that sends a notification as a reminder to look away from the screen far into the distance.  
The purpose is to exercise the eye muscles as myopia (nearsightedness) is increasingly  
developed amongst people looking at screens for a prolonged amount of time every day.  
Exercising the muscles may help prevent or slow down the progression of myopia.

Reminder interval as well as how long you should look away are configurable.  
In addition, you can also add application or window names, and you will not be disturbed if they are running.

Currently, notifications will not be sent if:  

* The system is idle.
* The microphone is active (configurable on/off).
* Blacklisted application or window is running (configurable).

Tested only on X11, Xubuntu 20.04 LTS and pulseaudio.   
It is likely it will not work on Wayland or PipeWire.

## Installing

_**Ubuntu 20.04**_ (Newer versions will not work as they use Wayland)
<font size="2">_(should automatically install with package)_</font>
```commandline
add-apt-repository ppa:lyubo-angelov/eyecare-reminder
apt-get update
apt install python3-eyecare-reminder
```

### Dependencies
<font size="2">_(should automatically install with package)_</font>
```
python3-pyqt5
python3-yaml
python3-psutil
python3-jeepney
python3-xdg
x11-utils
pulseaudio-utils
xprintidle
```

## Usage

Upon launching, a system tray icon will be added.  
Clicking it should bring up a menu with a few options.

* _**Edit config**_ - opens the config file with the default text editing application set on the system.
* _**Reload config**_ - reloads the config file. Must be run after editing config to pick up new changes.
* _**Open log**_ - opens the log with the default text editing application set on the system.
* _**Reset to default**_ - reset the config file to default.  
* _**Autostart**_ - Enable/Disable autostart on login, _**only works on Gnome**_.
* _**Exit**_ - exits the app.

The default settings are set to bring up a notification every 20 mins,  
with 2 minutes of looking into the distance after which another notification is brought up    
to signify that looking at the screen may be resumed.

### Config file

* _**enable_sound**_ - "true" or "false". Enables or disables the sound of the notifications.
* _**suppress_when_microphone_active**_ - "true" or "false". Whether to ignore notifications when microphone is active.
* _**idle_time**_ - number of seconds after which system is considered idle.
* _**reminder_interval**_ - number of seconds after which the reminder notification is sent.
* _**reminder_cooldown_interval**_ - number of seconds to look into the distance. 2nd notification appears after this.
* _**blacklist_process_names**_ - eg. ["process_name1", "process_name2"] Ignore notifications if these are running.
* _**blacklist_window_names**_ - eg. ["window1", "window2"] Ignore notifications if any of these windows are open.

## Building from source
Clone this repository somewhere on your system.  
In a terminal navigate to that directory.  
Eg:
```commandline
git clone https://github.com/LyuboslavAngelov/eyecare-reminder.git
cd eyecare-reminder
```

Install build dependencies:  
<font size="1">_*May require root priviliges_</font>
```commandline
apt install dh-python python3-stdeb python3-xdg
```

### Building the deb package:
To build the deb package:
```commandline
make dist
```
To install the deb package to your system:  
<font size="1">_*May require root priviliges_  
_*It is important to note that this will attempt to install all runtime dependencies._</font>
```commandline
make install
```

To uninstall the deb package from your system:  
<font size="1">_*May require root priviliges_</font>
```commandline
make uninstall
```
## For developers:
### To make a local virtual environment and test changes on the fly:
To make a local virtual environment:  
<font size="1">_*It is important to note that this **will not install non python dependencies**_</font>
```commandline
make venv
```
To install the python module to the venv and launch the app:
```commandline
make launch
```
### Misc commands
To clean both venv and deb build files:
```commandline
make clean-all
```
To clean deb build files:
```commandline
make clean-dist
```
To clean venv files:
```commandline
make clean-venv
```

## Credits
* Sounds from [Notification Sounds](https://notificationsounds.com/)
* Icon from [ICONS8](https://icons8.com)

## License

**GNU GENERAL PUBLIC LICENSE Version 3**  
  
<font size="">_More information in the LICENSE file_</font>
