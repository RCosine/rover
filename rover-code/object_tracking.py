"""
Based off of the code of Jitesh Saini - Github https://github.com/jiteshsaini, Project name AI Robot - Object Tracking
Edits made for the mecanum wheels, and no Coral USB Accelerator

"""

import common as cm
import cv2
import numpy as np
from PIL import Image
import time
import os
import sys
from threading import Thread

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
import util as ut
ut.init_gpio()

# obstacle avoidance

from obstacle_avoidance import ObstacleAvoidance, override_active
avoider = ObstacleAvoidance()
avoider.start()

motor_thread = None # this prevents issues with threads

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

threshold = 0.2
top_k = 5 # number of objects to be shown as detected, probably will lower

# model paths

model_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'models')
model = 'mobilenet_ssd_v2_coco_quant_postprocess.tflite'
model_edgetpu = 'mobilenet_ssd_v2_coco_quant_postprocess_edgetpu.tflite'
lbl = 'coco_labels.txt'

tolerance = 0.1
x_deviation = 0
y_deviation = 0
arr_track_data = [0,0,0,0,0,0]

# objects that robot will track, edit whenever, see models/coco_labels.txt for 80 objects!

arr_valid_objects = ['banana','apple','orange'] # yeah all I got are fruits

# mecanum wheels take 5V for full speed

def track_object(objs,labels):
    global x_deviation, y_deviation, tolerance, arr_track_data, motor_thread
    
    if (len(objs) == 0):
        ut.stop()
        ut.red_light("OFF")
        arr_track_data = [0,0,0,0,0,0]
        return
    
    k = 0
    flag = 0
    for obj in objs:
        lbl = labels.get(obj.id, obj.id)
        k = arr_valid_objects.count(lbl)
        
        if (k > 0):
            x_min, y_min, x_max, y_max = list(obj.bbox)
            flag = 1
            break
        
    if (flag == 0):
            return
        
    x_diff = x_max - x_min
    y_diff = y_max - y_min
        
    obj_x_center = round(x_min + (x_diff / 2), 3)
    obj_y_center = round(y_min + (y_diff / 2), 3)
    
    x_deviation = round(0.5 - obj_x_center, 3)
    y_deviation = round(0.5 - obj_y_center, 3)
    
    arr_track_data[0] = obj_x_center
    arr_track_data[1] = obj_y_center
    arr_track_data[2] = x_deviation
    arr_track_data[3] = y_deviation
    
    # check that a motor thread is active before making a new one
    
    if motor_thread is None or not motor_thread.is_alive():
        motor_thread = Thread(target=move_robot)
        motor_thread.start()
        
def move_robot():
    global x_deviation, y_deviation, tolerance, arr_track_data
    
    if override_active.is_set(): # obstacle avoidance
        return
    
    if (abs(x_deviation) < tolerance and abs(y_deviation) < tolerance):
        cmd = "Stop"
        delay1 = 0
        ut.stop()
        ut.red_light("ON")
        
    else:
        ut.red_light("OFF")
        if abs(x_deviation) > abs(y_deviation):
            if (x_deviation >= tolerance):
                cmd = "Move Left"
                delay1 = get_delay(x_deviation, 'l')
                ut.left()
                time.sleep(delay1)
                ut.stop()
                
            elif (x_deviation <= -1 * tolerance):
                cmd = "Move Right"
                delay1 = get_delay(x_deviation, 'r')
                ut.right()
                time.sleep(delay1)
                ut.stop()

        else:
            
            if (y_deviation >= tolerance):
                cmd = "Move Forward"
                delay1 = get_delay(y_deviation, 'f')
                ut.forward()
                time.sleep(delay1)
                ut.stop()
                
            elif (y_deviation <= -1 * tolerance):
                cmd = "Move Backward"
                delay1 = get_delay(y_deviation, 'b')
                ut.back()
                time.sleep(delay1)
                ut.stop()
    
    arr_track_data[4] = cmd
    arr_track_data[5] = delay1

# based off of the deviation of the object from the frame's center, a delay value is returned, which decides how long the motion command is given to the motors

def get_delay(deviation, direction):
    deviation = abs(deviation)
    if (direction == 'f' or direction == 'b'):
        if (deviation >= 0.3):
            d = 0.1
        elif (deviation >= 0.2 and deviation < 0.30):
            d = 0.075 
        elif (deviation >= 0.15 and deviation < 0.2):
            d = 0.045
        else:
            d = 0.035
    else :
        if (deviation >= 0.4):
            d = 0.080
        elif (deviation >= 0.35 and deviation < 0.40):
            d = 0.070
        elif (deviation >= 0.30 and deviation < 0.35):
            d = 0.060
        elif (deviation >= 0.25 and deviation < 0.30):
            d = 0.050
        elif (deviation >= 0.20 and deviation < 0.25):
            d = 0.040
        else:
            d = 0.030
            
    return d

def main():
    from util import edgetpu

    if (edgetpu == 1):
        mdl = model_edgetpu
    else:
        mdl = model
    
    interpreter, labels = cm.load_model(model_dir, mdl, lbl, edgetpu)
    
    fps_count = 0
    last_print = time.time()
    
    try:
        while True:
            start_time = time.time()
            
            # capture camera frame
            
            ret, frame = cap.read()
            if not ret:
                time.sleep(0.01)
                continue
                
            cv2_im_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_im = Image.fromarray(cv2_im_rgb)
            
            cm.set_input(interpreter, pil_im)
            interpreter.invoke()
            objs = cm.get_output(interpreter, score_threshold=threshold, top_k=top_k)
            
            track_object(objs, labels)
            
            fps_count += 1
            if time.time() - last_print >= 1.0:
                cmd = arr_track_data[4]
                x_dev = arr_track_data[2]
                y_dev = arr_track_data[3]
                print(f"FPS: {fps_count} | Command: {cmd} (X: {x_dev}, {y_dev})")
                fps_count = 0
                last_print = time.time()
          
    except KeyboardInterrupt:
        print("shut down")
    finally:
        ut.stop()        
        cap.release()

if __name__ == '__main__':
    main()
    
