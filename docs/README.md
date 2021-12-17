## Links

- [How to use WS2812B RGB LEDs with Raspberry Pi](https://www.youtube.com/watch?v=Pxt9sGTsvFk)
- [WS2812 / NeoPixel Addressable LEDs: Raspberry Pi Quickstart Guide](https://core-electronics.com.au/tutorials/ws2812-addressable-leds-raspberry-pi-quickstart-guide.html)

## Hardware

I got everything off Amazon.

- [Shopping List](https://www.amazon.com/hz/wishlist/ls/382JJL74JTTD9?ref_=wl_share)

## Software

### ANT+ Client

- [libant](https://github.com/half2me/libant)


### Programmable LEDs

```
#!/bin/bash

# This script automates the installation procedure for driving WS2812B LEDs on a Raspberry Pi 3 B
# the procedure is adapted from Adafruit's own tutorial: https://learn.adafruit.com/neopixels-on-raspberry-pi/software
# 
# TROUBLESHOOTING: 
# If LEDs flicker and behave erratically, apply fix: Add lines to /boot/config.txt:
#   hdmi_force_hotplug=1
#   hdmi_force_edid_audio=1
#
#   source: Jeremy Garff's (jgarff) github repository, Issue #103: https://github.com/jgarff/rpi_ws281x/issues


# Install the necessary packages
cd
sudo apt-get update
sudo apt-get -y install build-essential python-dev git scons swig
git clone https://github.com/jgarff/rpi_ws281x.git
cd rpi_ws281x
scons

cd python
sudo python setup.py install
cd
```

```
curl -L http://coreelec.io/33 | bash
```