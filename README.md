
# rover

![banner](https://i.postimg.cc/y6wJx5x3/banner.png)

Welcome to Rover! Rover is a simple object tracking vehicle that uses a Raspberry Pi running object detection models. Rover can also be used in a manual control mode, where you can drive it through a Flask web app and see first person footage from the camera on the body. Rover uses 3D printed parts for the chassis. I created this project because I wanted to add a unique twist to the classic obstacle-avoiding rover project. This version brings actual intelligence to the rover, and the ultrasonic sensor is now being used to make sure the rover doesn't hit anything while it's following an object.

The footprint of Rover is approximately 192mm x 192mm x 110 mm.

## Navigating this repo

- For **images** and to see a 3D model, scroll below.
- To get the **code** for the rover, go to the /rover-code folder.
- To access the files for **3D printing**, go in /models and download the file format you want that starts with "print-" (there's a rover-model.step that isn't for printing).
- **Instructions** for setting up the rover will be in [instructions.md](./instructions.md).
- To see my **thought process** in working on this project, go to /journals.
- The **bill of materials** is at [bill-of-materials.csv](./bill-of-materials.csv).
- The **wiring diagram** is at [wiring-diagram.png](./wiring-diagram.png)

## Details

### Images

| Front | Back | Top | Bottom | Inside |
| --- | --- | --- | --- | --- |
| ![Front](./images/Screenshot-2026-08-07-at-12-09-07-PM.png) | ![Back](./images/Screenshot-2026-08-07-at-12-09-13-PM.png) | ![Top](./images/Screenshot-2026-08-07-at-12-09-25-PM.png) | ![Bottom](./images/Screenshot-2026-08-07-at-12-09-21-PM.png) | ![Inside](./images/Screenshot-2026-08-07-at-12-09-39-PM.png) |

*Important note about images: the camera module in these pictures is a different one than the one listed in the Bill of Materials, reason being that I couldn't find the right model.*

To view an online-hosted 360 degree view of this robot, click [here](https://viewer.autodesk.com/id/dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6YTM2MHZpZXdlci1wcm90ZWN0ZWQvdDE3ODYxMzAxMDFfZWQ1MWQwMjQtYmZkZC00ODYwLTlhMmEtNWNkMTA2MTk2NTlkLnN0ZXA?sheetId=MDg1ZTA2MzItN2NhZS00OWVhLThhOTYtMDhkMjE2MTU4ZDQ1). The same file is in the /models folder ([here](./models/rover-model.step)). If the online-hosted link expires for any reason, please let me know by opening an issue request.

### Bill of Materials

| Item # | Component | Quantity | Price ($) | Vendor | URL | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 80mm Mecanum Wheels (Set of 4) | 1 | 19.21 | AliExpress | [Link](https://www.aliexpress.us/item/3256804929248374.html) | Sold as a 4-pack set designed to fit TT motors |
| 2 | 1:220 TT Motors (Set of 4) | 1 | 6.93 | AliExpress | [Link](https://www.aliexpress.us/item/3256808093084021.html) | Sold as a 4-pack set; rated for 6V (restrict PWM in driver) |
| 3 | Ultrasonic Sensor | 1 | 2.95 | AliExpress | [Link](https://www.aliexpress.us/item/3256812540803651.html) | 3.3V compatible distance sensor |
| 4 | Raspberry Pi 3 Model A+ | 1 | 25.00 | Adafruit | [Link](https://www.adafruit.com/product/4027) | Main single-board computer |
| 5 | DFRobot Motor Driver Expansion Board | 1 | 34.25 | AliExpress | [Link](https://www.aliexpress.us/item/3256807075492551.html) | Motor driver shield (free shipping option) |
| 6 | M2.5 Spacers Kit + M2.5 6mm Screws | 1 | 9.26 | AliExpress | [Link](https://www.aliexpress.us/item/3256807311842711.html) | Standoff hardware kit including 6mm screws |
| 7 | Wide-Lens Camera Module (Color I 130) | 1 | 6.19 | AliExpress | [Link](https://www.aliexpress.us/item/2251832482194239.html) | Color I 130 wide-angle camera module |
| 8 | SG90 Servo Motor | 1 | 2.47 | AliExpress | [Link](https://www.aliexpress.us/item/3256806097043668.html) | Servo motor for LiDAR scanning assembly |
| 9 | Samsung 25R 18650 2500mAh 20A Battery | 2 | 10.00 | 18650 Battery Store | [Link](https://www.18650batterystore.com/products/samsung-25r-18650?_pos=1&_sid=a19e8e6a9&_ss=r) | 2x Unprotected cells ($5.00 each) |
| 10 | 18650 Battery Store Shipping | 1 | 7.41 | 18650 Battery Store | [Link](https://www.18650batterystore.com/products/samsung-25r-18650?_pos=1&_sid=a19e8e6a9&_ss=r) | Store shipping fee ($17.41 total battery order) |
| 11 | 2x18650 Battery Storage Box (7.4V) | 1 | 2.32 | AliExpress | [Link](https://www.aliexpress.us/item/3256811664143308.html) | Battery holder with DC jack output for 2S |
| 12 | M2.5 Screws (12mm) | 1 | 2.05 | AliExpress | [Link](https://www.aliexpress.us/item/3256808523663879.html) | M2.5 x 12mm screws |
| 13 | Dupont Cables (F-M 40cm, 20-pack) | 1 | 1.74 | AliExpress | [Link](https://www.aliexpress.us/item/3256804460701476.html) | Female-to-Male jumpers (20-pack) |
| 14 | 18650 Battery Charger (2 Slots) | 1 | 6.77 | AliExpress | [Link](https://www.aliexpress.us/item/3256806967255191.html) | Dual-slot lithium-ion battery charger |
| **TOTAL** | **Grand Total** | **15** | **136.55** | | | **All electronic components + battery shipping included** |

### Wiring Diagram

Below is the wiring diagram to help you connect the motors, sensors, batteries, and the Raspberry Pi with the Motor Driver:

![Wiring Diagram](./wiring-diagram.png)

### Instructions

Please go to the dedicated [instructions.md](./instructions.md) file to see instructions.
