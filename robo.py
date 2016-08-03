import ConfigParser
import cv2
from flask import Flask
from flask import render_template
from flask import Response
import json
import NetworkManager
import os
import optparse
from time import sleep
from threading import Thread
config = ConfigParser.ConfigParser()
config.readfp(open('/etc/sumochip/sumochip.conf'))

#Creating path and folders
class MotorThread(Thread):
    def __init__(self, pin=192):
        #print("Instantiating motor thread at pin %d" % pin)
        Thread.__init__(self)
        self.path = "/sys/class/gpio/gpio%d" % pin
        if not os.path.exists(self.path):
            with open("/sys/class/gpio/export", "w") as fh:
                fh.write(str(pin))
        with open(os.path.join(self.path, "direction"), "w") as fh:
            fh.write("out")
        self.speed = 0
        self.daemon = True
    def run(self):
        with open(os.path.join(self.path, "value"), "w") as fh:
          while True:
            if self.speed:
                fh.write("1")
                fh.flush()
                sleep(0.002 if self.speed > 0 else 0.001)
                fh.write("0")
                fh.flush()
                sleep(0.018 if self.speed > 0 else 0.019)
            else:
                sleep(0.020)

#Defining left and right motors
left = MotorThread(config.getint('pins', 'motor left'))
left.start()
right = MotorThread(config.getint('pins', 'motor right'))
right.start()

app = Flask(__name__ )

#Setting up and getting network information
@app.route("/api/wireless", methods=['GET', 'POST'])
def wireless():
    networks = []    
    for dev in NetworkManager.NetworkManager.GetDevices():
        if dev.DeviceType != NetworkManager.NM_DEVICE_TYPE_WIFI:
            continue
    for ap in dev.SpecificDevice().GetAccessPoints():
        networks.append({"ssid":ap.Ssid, "freq":ap.Frequency, "strength":ord(ap.Strength)})
        return json.dumps(networks)

#Making robot controls, just in scratch
@app.route("/left")
def command():
    left.speed = 1
    right.speed = -1
    return "left"

@app.route("/stop")
def stop():
    left.speed = 0
    right.speed = 0
    return "stop"

@app.route("/go")
def go():
    left.speed = 1
    right.speed = 1
    return "go"

@app.route("/right")
def right1():
    left.speed = -1
    right.speed = 1
    return "right"

@app.route("/back")
def back():
    left.speed = -1
    right.speed = -1
    return "back"

