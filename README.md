# metro-stm-indicator
Unity Indicator displaying the STM metro status (Montréal)

![Screencap](https://raw.githubusercontent.com/pc-coholic/metro-stm-indicator/master/screencap.png)

## Installation
* Use Ubuntu (or any other OS, that uses unity/gnome3-style indicator-bar)
* Clone the repo or download the tarball/[zipball](https://github.com/pc-coholic/metro-stm-indicator/archive/master.zip) and place/extract in a convienient location - for example /opt/metro-stm-indicator
* Install the necessary dependencies:
 * python
 * pygtk >=2.0
 * gtk
 * appindicator
 * gobject
 * urllib2
 * xmltodict
 * json
 * io
 * subprocess
 * aplay
* Edit - if desired config.json to select the desired language: "Anglais" or "Francais".
* launch metro-stm-indicator.py
* Optional: place metro-stm-indicator.py.desktop in your autostart-folder (~/.config/autostart/ or /home/\<user\>/.config/autostart/ or similar)

## Usage
Launch metro-stm-indicator.py by hand or automatically. Get a notification when there is a problem with the metro.

## Known problems
* Messy code
* No pypi-package or install-routine
* No config-switch to mute the audio-signal

