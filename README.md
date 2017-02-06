# lighting-augmentation
Arduino controlled LED lighting to augment deep learning models

**Circular Lighting:**
* This works awesome. It was last trick in getting one shot networks for coin designs. 

Frames are captured with a different lighting angles as the part is moving under the camera. A 24 LED(WS2812) strip in a 50mm circle is switched every 50ms. 2 LEDs are on at all times. So as the coin is moving on  the belt 13-19 captures are done. It's pretty sloppy as I have yet to even sync the image capture and LED switching, but it works great!


**Later Tasks:**
Try 3 color channels in the LED to scan 3 angles at once! Also I could take all lights on pictures, and pictures with lights different heights. Not fancy, just 3 light strips loops. One loop horizontal, one vertical, and one under for separate backlighting shots. They don’t have to be mounted perfectly. The LEDs can switch every frame. You check the every n frames to see if the times is correct. The belt would always be moving. So both the camera and the lighting would be different models. I could make the models every image for itself then I could ensemble them. This is cool because it will show when the models are bad. The reason for this is also because this setup is going to work not just for coins, but other part types as well with no changes.

**Back lighting Tasks**:
* Scan screws without an image at all:1 bit backlighting from 8 different angles would the same as 256 gray but really it should be blob input instead of an image. 
* You could have 25 different backlighting channels with cameras on top and bottom with the frosted belt. This is sloppy 3d scanning without doing the math. 
* This will work for sure with the screws not touching, but can be it work with the screws touching?
* An old flat panel display can be both the backlight and it can light up around the issue screws.
