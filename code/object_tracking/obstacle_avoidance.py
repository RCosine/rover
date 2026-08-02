"""
this script is for the servo motor and ultrasonic sensor
based off of earthrover/range_sensor/avoid_collision.py and earthrover/range_sensor/range_sensor.py
also based off of adeept/adeept_picar-b — server/ultra.py
for a 3.3V ultrasonic sensor ONLY
the servo motor is connected to the HAT

had to use AI for the servo motor part (the motor driver  is very annoying)
functionality is that the robot won't hit anything while tracking, if it detects an obstacle, it will stop and wait until the object moves away from obstacle or obstacle moves

the pin layout is:
for ultrasonic sensor: VCC - Pin 1, GND - Pin 6, TRIG - 16 (GPIO 23 Output), ECHO - 18 (GPIO 24 3.3v)
for servo motor: S1 header on DFRobot DRI0054 HAT (I2C Address 0x60)

"""

import RPi.GPIO as GPIO
import time
import threading
import os
import sys
import util as ut

# GPIO pin assigning

TRIG = 23 # pin 16
ECHO = 24 # pin 18 (3.3v connection)

OBSTACLE_THRESHOLD = 25.0 # safety distance threshold in cm
CLEAR_THRESHOLD = 30.0 # robot resums when distance exceeds this in cm 
override_active = threading.Event() # override for code to pause when obstacle is near

# measure distance

def measure_distance():
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)
    
    start_time = time.time()
    stop_time = time.time()
    timeout = start_time + 0.03 # 30ms timeout
    
    # wait for ECHO to go HIGH
    
    while GPIO.input(ECHO) == 0:
        start_time = time.time()
        if start_time > timeout:
            return 999.0
        
    # wait for ECHO to go LOW
    
    while GPIO.input(ECHO) == 1:
        stop_time = time.time()
        if stop_time > timeout:
            return 999.0
        
    time_elapsed = stop_time - start_time
    distance = (time_elapsed * 34300) / 2
    return round(distance, 1)

# take multiple readings and filter out noise

def get_median_distance(samples = 3):
    readings = []
    for _ in range(samples):
        readings.append(measure_distance())
        time.sleep(0.01)
    readings.sort()
    return readings[samples // 2]
    
class ObstacleAvoidance(threading.Thread):
    def __init__(self):
        super().__init__()
        self.daemon = True
        
        ut.init_gpio()
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(TRIG, GPIO.OUT)
        GPIO.setup(ECHO, GPIO.IN)
        GPIO.output(TRIG, False)
        
        ut.set_servo_direction('stop')
        time.sleep(0.5)
                
    def run(self):
        print("obstacle check running")
        was_blocked = False
        
        while True:
            dist = get_median_distance(3)
            current_dir = ut.current_direction
            
            if dist < OBSTACLE_THRESHOLD and not override_active.is_set():
                override_active.set() # pause object tracking
                ut.stop()
                was_blocked = True
                print(f"Obstacle at {dist:.1f}cm, waiting for clearance")
            
            elif dist > CLEAR_THRESHOLD and override_active.is_set():
                override_active.clear()
                was_blocked = False
                print(f"Path clear ({dist:.1f}cm, resuming tracking)")
                
            elif override_active.is_set():
                ut.stop()
                if was_blocked:
                    print(f"Still blocked ({dist:.1f}cm, waiting for clearance)")
                    was_blocked = False
                    
            time.sleep(0.1)

if __name__ == '__main__':
    ut.init_gpio()
    print("testing obstacle avoidance")
    print(f"stop threshold: {OBSTACLE_THRESHOLD}cm; resume threshold: {CLEAR_THRESHOLD}cm")
    print("tesing servo sweep")
    
    for direction in ['forward', 'left', 'right', 'rotate_left', 'rotate_right', 'stop']:
        print(f" setting direction to: {direction} (angle: {ut.SERVO_ANGLES[direction]}deg)")
        ut.set_servo_direction(direction)
        time.sleep(1) 
        d = get_median_distance()
        print(f" distance: {d:.1f} cm")
        
    print("put your hand in front of sensor to test \n") 
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)
    GPIO.output(TRIG, False)
    
    blocked = False
    try:
        while True:
            d = get_median_distance()
            dir_str = ut.current_direction
            if d < OBSTACLE_THRESHOLD and not blocked:
                print(f"blocked - {d:.1f}cm")
                blocked = True
            elif d > CLEAR_THRESHOLD and blocked:
                print(f"clear - {d:.1f}cm")
                blocked = False
            elif not blocked:
                print(f"ok - {d:.1f}cm")
            time.sleep(0.3)
            
    except KeyboardInterrupt:
        ut.stop()
        GPIO.cleanup()
        print("\n done")
        
        if (script )