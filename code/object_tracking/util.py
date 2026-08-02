"""
adapted for mecanum wheels, original project Earthrover by Jitesh Saini
I used AI to help fix this part because I got stuck with managing the driver board
uses DFRobot DRI0054 Motor Driver HAT over I2C 
 
"""

import os
import time
import sys

edgetpu = 0 # set to 0 because no coral usb accelerator

# motor hat 

sys.path.append(os.path.join(os.path.dirname(__file__), 'DFRobot_RaspberryPi_Motor'))
try:
    from DFRobot_RaspberryPi_Motor import DFRobot_RaspberryPi_Motor as Board
except ImportError:
    
    # fallback class to prevent code crashing when testing on laptop that doesn't have I2C libary installed
    
    class Board:
        M1 = 1
        M2 = 2
        M3 = 3
        M4 = 4
        CW = 1
        CCW = 2
        ALL = 0
        def begin (self): pass
        def set_moter_pwm_frequency(self, freq): pass
        def motor_movement(self, ids, orientation, speed): pass
        def motor_stop (self, motor_id): pass
        def set_servo_angle(self, servo_id, angle): pass
        
board = None
SPEED = 80 # this is default motor speed
current_direction = 'stop'

# servo angles for sensor detection

SERVO_ANGLES = {
    'forward': 90,
    'back': 90,
    'left': 150,
    'right': 30,
    'rotate_left': 90,
    'rotate_right': 90,
    'stop': 90
}

# sets up the driver hat over I2C

def init_gpio():
    global board
    try:
        board = Board()
        board.begin()
        board.set_moter_pwm_frequency(1000)
        print("DFRobot Motor HAT initialized on I2C (Address 0x60)")
        set_servo_direction('stop')
    except Exception as e:
        print(f"Warning: Could not initialize DFRobot Motor Hat: {e}")

# stop all motors

def stop():
    global current_direction
    current_direction = 'stop'
    if board:
        try:
            board.motor_stop(Board.ALL)
            set_servo_direction('stop')
        except Exception:
            pass

# steer servo to face direction of movement

def set_servo_direction(direction):
    if board is None:
        return
    angle = SERVO_ANGLES.get(direction, 90)
    try:
        board.set_servo_angle(1, angle)
    except Exception as e:
        pass

# 4 motor direction: 1 = c (forward), -1 = cc (backward), 0 = stop

def _set_motors(fl, fr, bl, br, direction = 'stop'):    
    global current_direction
    current_direction = direction
    set_servo_direction(direction)
    
    if board is None:
        return

    motors = [(Board.M1, fl), (Board.M2, fr), (Board.M3, bl), (Board.M4, br)]
    
    for motor_id, dir_val in motors:
        if dir_val == 1:
            board.motor_movement([motor_id], Board.CW, SPEED)
        elif dir_val == -1:
            board.motor_movement([motor_id], Board.CCW, SPEED)
        else:
            board.motor_stop(motor_id)

def forward(): # all wheels forward
    _set_motors(1, 1, 1, 1, direction = 'forward')
    
def back(): # all wheels backward
    _set_motors(-1, -1, -1, -1, direction = 'back')

def left(): # strafe left
    _set_motors(-1, 1, 1, -1, direction = 'left')

def right(): # strafe right
    _set_motors(1, -1, -1, 1, direction = 'right')
    
def rotate_left(): # rotate cc 
    _set_motors(-1, 1, -1, 1, direction = 'rotate_left')

def rotate_right(): # rotate c
    _set_motors(1, -1, 1, -1, direction = 'rotate_right')
        
def set_speed(speed_val): # sets motor speed 0 - 100%
    global SPEED
    SPEED = max(0, min(100, int(speed_val)))

def red_light(state):
    pass

def camera_light(state):
    pass

def head_lights(state):
    pass
