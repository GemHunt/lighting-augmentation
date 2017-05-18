# lighting-augmentation
Arduino controlled LED lighting to augment deep learning models

Check out the video on YouTube

This repo is to demonstrate using Arduino controlled LED lighting to augment deep learning models. 

This works awesome. The first time I used this got 100% accuracy determining head vs tails on a 1000 images of different coins(same design) with no manual training. 

**To reproduce the results:**
Download the dataset: http://www.gemhunt.com/cents.tar

**Dataset Scanning Details:**
(57,000 images, 56x56 PNG files, 342MB Total, 1000 coins each with 57 different lighting angles)
The images were captured using: https://github.com/GemHunt/real-time-coin-id/blob/master/scanning.py
Frames were captured with different lighting angles as the coin is moving stopped under the camera. Just above the coin is a 18 LED (WS2812) strip in a 50mm circle. Around the camera there are 8 more, so this makes 26 total. Every 30ms the lighting is changed. So each of these 26 lights are on one at a time, then all bottom lights, then all top lights. So 28 different lighting combinations. It's pretty sloppy as the image capture is not synced to the LED switching, but it works great! I'm guessing this works similar to using depth maps from 3D scanning into the neural network model.

The Arduino ino used is at:
https://github.com/GemHunt/CoinSorter/blob/master/hardware/scanner-sorter/led_and_solenoid_control/led_and_solenoid_control.ino
A simpler version without motor and solenoid control is in this repo. 

**Later Tasks:**
* Try 3 color channels in the LED to scan 3 angles at once. 

**Back lighting Tasks:**
* Add backlighting to the image set. Using the LED strips under the belt makes for a very clean outline of more complex parts. 
* Scan screws without an image at all:1 bit backlighting from 8 different angles would the same as 256 gray but really it should be blob input instead of an image.
* Try training sets with parts touching.
* In a tray configuration, an old flat panel display can be both the backlight and light up around the issue parts.
