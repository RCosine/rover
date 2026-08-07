"""
flaskweb ui for manual robot control with camera fpv
based heavily off of:
EbenKouao/pi-camera-stream-flask (https://github.com/EbenKouao/pi-camera-stream-flask)
jiteshsaini/robotics-level-4 — earthrover/control_panel/remote.js (https://github.com/jiteshsaini/robotics-level-4)
neptune46/RaspiWebCar/webcar.py (https://github.com/Neptune46/RaspiWebCar/blob/master/webcar.py)

"""

from flask import Flask, render_template, Response, jsonify
import cv2

class VideoCamera(object):
    def __init__(self, flip=False): # set to true if the camera is upside down
        self.vs = cv2.VideoCapture(0)
        self.vs.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
        self.vs.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
        self.flip = flip
    
    def __del__(self):
        self.vs.release()
        
    def get_frame(self):
        success, frame = self.vs.read()
        if not success:
            return b''
        if self.flip:
            frame = cv2.flip(frame, 0)
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()

pi_camera = VideoCamera(flip = False)

# motor control

import util
util.init_gpio()

# app globals (don't edit)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('manual.html')

# get camera frame

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(pi_camera), mimetype = 'multipart/x-mixed-replace; boundary=frame')

# motor commands

@app.route('/fwd')
def go_fwd():
    util.forward()
    return jsonify(result="ok")

@app.route('/back')
def go_back():
    util.back()
    return jsonify(result="ok")

@app.route('/left')
def go_left():
    util.left()
    return jsonify(result="ok")

@app.route('/right')
def go_right():
    util.right()
    return jsonify(result="ok")

@app.route('/stop')
def go_stop():
    util.stop()
    return jsonify(result="ok")

@app.route('/rotate_left')
def go_rotate_left():
    util.rotate_left()
    return jsonify(result="ok")

@app.route('/rotate_right')
def go_rotate_right():
    util.rotate_right()
    return jsonify(result="ok")

@app.route('/strafe_fwd_left')
def go_strafe_fwd_left():
    util._set_motors(0, 1, 1, 0)
    return jsonify(result="ok")

@app.route('/strafe_fwd_right')
def go_strafe_fwd_right():
    util._set_motors(1, 0, 0, 1)
    return jsonify(result="ok")

@app.route('/strafe_back_left')
def go_strafe_back_left():
    util._set_motors(-1, 0, 0, -1)
    return jsonify(result="ok")

@app.route('/strafe_back_right')
def go_strafe_back_right():
    util._set_motors(0, -1, -1, 0)
    return jsonify(result="ok")

if __name__ == "__main__":
    app.run(host = '0.0.0.0', port = 2205, debug = False)