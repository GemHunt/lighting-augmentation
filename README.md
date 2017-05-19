# lighting-augmentation
Arduino controlled LED lighting to augment deep learning models

Check out the video on YouTube

**Repo Goals**
* To demonstrate using Arduino controlled LED lighting to augment deep learning models
* To show how this is very simple, quick, and low cost unsupervised method of grouping 3D surfaces
* To find ways to make this process better (Feel free ask questions or comments in the Issues) 
* To show off one of the simple building blocks off unsupervised anomaly detection

With the current data set this gets 98-100% accuracy determining head vs tails on a 1000 different coins(same design) with no manual training. 

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
* 57 images of each coin are captured from mostly different lighting angles  
* HoughCircles is done on all 57 images
* The centers are averaged and the images are cropped down to 56x56
* No camera calibration
* ![gif](https://github.com/GemHunt/lighting-augmentation/blob/master/1100.gif "gif")

**Training Data Set Creation Pipeline**
* 2 coins are labeled(one heads, one tails) 
* 57 x 100 = 5700 training images are created with lighting, rotation, and center jittering augmentations
* 56x56:  57 different lighting angles 
* 42x42: A 42x42 square is cropped 100 random rotations 
    with the crop center is randomly jittered in a 2x2 pixel window
* 28x28: Resize to 28x28
* ![training-data](https://github.com/GemHunt/lighting-augmentation/blob/master/training-data.png "training-data")

**Inference Pipeline**
* A model is created from this training data set
* All 57000 images are inferred
* The 57 results for each coin are summed

**Dataset Scanning Details:**
(57,000 images, 56x56 PNG files, 342MB Total, 1000 coins each with 57 different lighting angles)
The images were captured using: https://github.com/GemHunt/real-time-coin-id/blob/master/scanning.py
Frames were captured with different lighting angles as the coin is moving stopped under the camera. Just above the coin is a 18 LED (WS2812) strip in a 50mm circle. Around the camera there are 8 more, so this makes 26 total. Every 30ms the lighting is changed. So each of these 26 lights are on one at a time, then all bottom lights, then all top lights. So 28 different lighting combinations. It's pretty sloppy as the image capture is not synced to the LED switching, but it works great! I'm guessing this works similar to using depth maps from 3D scanning into the neural network model.

**Ignored in this repo:**
* There are 2 cameras that scan each side of the coin.
* (Even ID) is the opposite side of (Even ID) + 3. 
* For example 124 is the opposite side of 127. 
* So really this is a data set of 500 coins with 2 images per coin. 

**The Arduino ino used is at:**
https://github.com/GemHunt/CoinSorter/blob/master/hardware/scanner-sorter/led_and_solenoid_control/led_and_solenoid_control.ino
A simpler version without motor and solenoid control is in this repo. 

**FAQ**
* With the correct lighting can't you just use template matching? Yes, but this is more quick, robust, and retains much more detail. 
* Your demo is One-Shot, not unsupervised? True, if you add a few more steps in software it would be unsupervised. I wanted to keep the demo as simple as possible.


**Questions I have:**
* What do you want to use this for?
* How useful is this?
* Is there a better way?
* Who else is doing this?


**Tasks:**
* Try other part types!!!
* How much does the lighting-augmentation add? Try running without it. 
* Try rotating the coin instead (I am sure it will work the same, but it's 
* Try camera angle augmentation: Take pictures while the belt is moving(Stereo)(This works great too, but I need to set up better center finding to get it work better.) 
* Try camera angle augmentation: Try cameras on other angles. 
* Try 3 color channels in the LED to scan 3 angles at once. 

**Back lighting Tasks:**
* Add backlighting to the image set. Using the LED strips under the belt makes for a very clean outline of more complex parts. 
* Scan screws without an image at all:1 bit backlighting from 8 different angles would the same as 256 gray but really it should be blob input instead of an image.
* Try training sets with parts touching.
* In a tray configuration, an old flat panel display can be both the backlight and light up around the issue parts.


**Thanks Again for the Questions & Comments!**
* Paul Krush
* Carol Stream, IL, USA
* pkrush@gemhunt.com




