# lighting-augmentation
Arduino controlled LED lighting to augment deep learning models

Check out the video on YouTube

This repo is to demonstrate using Arduino controlled LED lighting to augment deep learning models. 

This works awesome. The first time I used this got 100% accuracy determining head vs tails on a 1000 images of different coins(same design) with no manual training. 

**To reproduce the results using Nvidia DIGITS:**
* Download the dataset: http://www.gemhunt.com/cents.tar
* Run label.py to randomly label one heads and one tails coin
* Build a caffe model (I use DIGITS, a gray 28x28 dataset, and LeNet)
* Download and untar the new model into ~/lighting-augmentation/heads_tails_model/
* Rename the *.caffemodel file to snapshot.caffemodel
* Run infer.py to classify the dataset
* Open lighting-augmentation-data/cents-labeled/results.png to view the results

**Scanning Pipeline:**
* The belt stops
* 57 images of each coin are captured
* From mostly different lighting angles  
* HoughCircles is done on all 57 
* The centers are averaged and the images are cropped down to 56x56
* No camera calibration

**Model Creation Pipeline**
* 2 coins are labeled(one heads, one tails) 
* 57 x 100 = 5700 training images are created with lighting,rotation, and center jittering augmentions:
* 56x56:  57 different lighting angles 
* 42x42: A 42x42 square is cropped 100 random rotations 
    with the crop center is randomly jittered in a 2x2 pixel window
* 28x28: Resize to 28x28
* This DataSet is trained with LeNet in DIGITS

**Dataset Scanning Details:**
(57,000 images, 56x56 PNG files, 342MB Total, 1000 coins each with 57 different lighting angles)
The images were captured using: https://github.com/GemHunt/real-time-coin-id/blob/master/scanning.py
Frames were captured with different lighting angles as the coin is moving stopped under the camera. Just above the coin is a 18 LED (WS2812) strip in a 50mm circle. Around the camera there are 8 more, so this makes 26 total. Every 30ms the lighting is changed. So each of these 26 lights are on one at a time, then all bottom lights, then all top lights. So 28 different lighting combinations. It's pretty sloppy as the image capture is not synced to the LED switching, but it works great! I'm guessing this works similar to using depth maps from 3D scanning into the neural network model.

Ignored in this repo: There are 2 cameras that scan each side of the coin. (Even ID) is the opposite side of (Even ID) + 3. For example 124 is the opposite side of 127. 

The Arduino ino used is at:
https://github.com/GemHunt/CoinSorter/blob/master/hardware/scanner-sorter/led_and_solenoid_control/led_and_solenoid_control.ino
A simpler version without motor and solenoid control is in this repo. 

**FAQ**
* With the correct lighting can't you just use template matching? Yes, but this is more quick, robust, and retains more detail. 

**Questions I have:**
* How useful is this?
* Is there a better way?
* Who else is doing this?
* How much better is just using 3D scanning? (This is so cheap I don't see a reason...)

**Tasks:**
* Try camera angle augmentation: Take pictures while the belt is moving.(Stero)
* Try camera angle augmentation: Try cameras on other angles. 
* Try 3 color channels in the LED to scan 3 angles at once. 

**Back lighting Tasks:**
* Add backlighting to the image set. Using the LED strips under the belt makes for a very clean outline of more complex parts. 
* Scan screws without an image at all:1 bit backlighting from 8 different angles would the same as 256 gray but really it should be blob input instead of an image.
* Try training sets with parts touching.
* In a tray configuration, an old flat panel display can be both the backlight and light up around the issue parts.







