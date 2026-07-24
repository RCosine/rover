Okay, so first thing is bringing the ultrasonic sensor back. I deleted the lidar one and uploaded the ultrasonic sensor. Then I have to update the BOM:

1. 4 80mm mecanum wheels - [https://www.aliexpress.us/item/3256804929248374.html](https://www.aliexpress.us/item/3256804929248374.html)
2. 4 1:220 TT Motors - [https://www.aliexpress.us/item/3256808093084021.html](https://www.aliexpress.us/item/3256808093084021.html)
3. Ultrasonic sensor (3.3v compatible) - [https://www.aliexpress.us/item/3256812540803651.html](https://www.aliexpress.us/item/3256812540803651.html)
4. Raspberry Pi 3 Model A+ - [https://www.adafruit.com/product/4027](https://www.adafruit.com/product/4027)
5. DF Robot Motor Driver Expansion Board - [https://www.aliexpress.us/item/3256807075492551.html](https://www.aliexpress.us/item/3256807075492551.html) or [https://www.dfrobot.com/product-2851.html](https://www.dfrobot.com/product-2851.html)
6. 12 mm M2.5 standoffs (spacers) + M2.5 screws
7. Wide-lens camera module - [https://www.aliexpress.us/item/2251832482194239.html](https://www.aliexpress.us/item/2251832482194239.html) (color I 130)
8. SG90 servo motor (for lidar sensor) - [https://www.aliexpress.us/item/3256806097043668.html](https://www.aliexpress.us/item/3256806097043668.html)
9. 2x 18650 2000mah 3.7v batteries - [https://www.aliexpress.us/item/3256808975352962.html](https://www.aliexpress.us/item/3256808975352962.html)
10. 2x18650 Battery Storage Box 7.4V - [https://www.aliexpress.us/item/3256811664143308.html](https://www.aliexpress.us/item/3256811664143308.html)

For the ultrasonic sensor, I have an idea for a unique mount that will make it look really cool. It's going to be like a semicircle and look high quality. First let me verify the size of the cad sensor and see if it matches. It should equal 20x45mm. It's 20.60 x 45.20. Interesting. I will design it around the bigger size, it'll fit the slightly smaller sensor anyways. How do I make a semicircle in a fusion sketch? After a search, it says use the Center Point Arc tool. The radius will be 23 mm. Then I stretched the arc 180 degrees and made a line across the bottom to make a semicircle:

![image](./images/pasted_20260724-223240.png)

The servo whole diameter is 2.0 mm so I will make a 2.4mm hole. Then I'll make a 5mm hole to allow the screw to go through the whole mount/

![image](./images/pasted_20260724-223846.png)

This is the sketch now I'll make it a body. (Extruding it like 22mm)

![image](./images/pasted_20260724-224400.png)

Here's the mount now, the front part will be to hold the "eyes" of the ultrasonic sensor.

![image](./images/pasted_20260724-224526.png)

Now, I'm going to trim the bottom of this to reduce the mass of the mount while still giving it that illusion of being whole. The radius is 23, so minus 3 mm is 20mm.

I messed up one of the measurements for making it hollow but I fixed it now:

![image](./images/pasted_20260724-225141.png)

Now to trim this out:

![image](./images/pasted_20260724-225219.png)

Amazing!

Now to cut out the eyeholes for the second part of this mount. I will make a sketch with circles of 1 mm extra than the "eyes" in CAD to be on the safe side. I'll then move it over to the mount and cut it out.

![image](./images/pasted_20260724-225539.png)

I'm having trouble finding the center of the circles here, so I'm going to try a different approach by overlaying a rectangle on it and finding the middle from there.

I deleted and then reimported the sensor to have it centered.

![image](./images/pasted_20260724-230111.png)

So I approximated one of the circles. Okay, now I did it to the other. I also deleted the raspberry pi model because it was getting annoying (it wouldn't hide when I isolated one of the bodies.)

![image](./images/pasted_20260724-230518.png)

This is the sketch now

Okay the mount front piece has been cut:

![image](./images/pasted_20260724-230704.png)

![image](./images/pasted_20260724-230943.png)

Okay neat. Now to move everything into its proper place. Moving the things gets annoying.

![image](./images/pasted_20260724-231416.png)

Wow, finally after a lot of moving, here it is!

Okay, now I have to make a cut into the front panel to let the camera chip move closer to the front.

I used questionable methods to find the center of the 4 holes, but I'm pretty confident it is the center:

![image](./images/pasted_20260724-231845.png)

(Top left corner of the composite rectangle)

![image](./images/pasted_20260724-232148.png)

Okay, so this is the back of the front panel now, Time to make the camera hole:

![image](./images/pasted_20260724-232625.png)

Okay, now I'm going to cut it out:

![image](./images/pasted_20260724-232652.png)

YES!

![image](./images/pasted_20260724-232814.png)

Here's the whole case again. I've decided I will push back making the rest of the screw holes as much as possible because that's my least favorite.

![image](./images/pasted_20260724-232954.png)

Regarding the back of the top lid, I think it doesn't actually need any magnets or mechanism to keep it in place because of how I initially designed it. It can sit on it's own completely flush with the other panels, and I can pick it up whenever I want to. This is great.

So basically, I only have the screw holes left to make and then some final design touches. And confirming everything before moving on.
