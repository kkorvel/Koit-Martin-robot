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
#print("sanity check")

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

class SensorThread(Thread):
    def __init__(self, pin =192):                                
        for pin  in range(192,196): 
            try:
                with open("/sys/class/gpio/export", "w") as fh:
                    fh.write(str(pin))
            except IOError:
                pass
            with open("/sys/class/gpio/gpio%d/direction" % pin, "w") as fh:
                fh.write("in")

class LightStrip(Thread):
    def __init__(self):                                
        for pin  in range(192,200): 
            try:
                with open("/sys/class/gpio/export", "w") as fh:
                    fh.write(str(pin))
            except IOError:
                 pass
            with open("/sys/class/gpio/gpio%d/direction" % pin, "w") as fh:
                fh.write("out")


    def on(self, pin):
        with open("/sys/class/gpio/gpio%d/value" % pin, "w") as fh:
            fh.write("0")

    def off(self, pin):
        with open("/sys/class/gpio/gpio%d/value" % pin, "w") as fh:
            fh.write("1")


strip = LightStrip()


left = MotorThread(config.getint('pins', 'motor left'))
left.start()
right = MotorThread(config.getint('pins', 'motor right'))
right.start()

app = Flask(__name__ )

@app.route("/batterystatus")
def battery():
    stats = {}
    #open the file battery to get the information about the battery
    for filename in os.listdir("/sys/power/axp_pmu/battery/"):
        with open ("/sys/power/axp_pmu/battery/" + filename) as fh:
            stats[filename] = int(fh.read())
            #r means read the values 
    with open("/sys/class/gpio/gpio203/value", "r") as fh:
        stats["enemy_left"] = int(fh.read())
        if stats['enemy_left'] == 1:
            reds_on()
        else:
            reds_off()
    with open("/sys/class/gpio/gpio193/value", "r") as fh:
        stats["line_left"] = int(fh.read())
    with open("/sys/class/gpio/gpio194/value", "r") as fh:
        stats["line_right"] = int(fh.read())
    with open("/sys/class/gpio/gpio200/value", "r") as fh:
        stats["enemy_right"] = int(fh.read())
        if stats['enemy_right'] == 1:
            blues_on()
        else:
            blues_off()

        
    return json.dumps(stats)

def reds_on():
    strip.on(198)
    strip.on(195)
    strip.on(194)
    strip.on(196)
def reds_off():
    strip.off(198)
    strip.off(195)
    strip.off(194)
    strip.off(196)

def blues_on():
    strip.on(197)
    strip.on(199)
    strip.on(193)
    strip.on(192)
def blues_off():
    strip.off(197)
    strip.off(199)
    strip.off(193)
    strip.off(192)

@app.route("/lightall")
def lightall():
    strip.on(197)
    strip.on(199)
    strip.on(193)
    strip.on(192)
    strip.on(198)
    strip.on(195)
    strip.on(194)
    strip.on(196)
    sleep(2)
    strip.off(197)
    strip.off(199)
    strip.off(193)
    strip.off(192)
    strip.off(198)
    strip.off(195)
    strip.off(194)
    strip.off(196)
    return "light"

@app.route("/light1")
def light1():
    strip.on(197)
    sleep(1)
    strip.off(197)
    return "light"
    
@app.route("/light2")
def light2():
    strip.on(199)
    sleep(1)
    strip.off(199)
    return "light"

@app.route("/light3")
def light3():
    strip.on(193)
    sleep(1)
    strip.off(193)
    return "light"

@app.route("/light4")
def light4():
    strip.on(192)
    sleep(1)
    strip.off(192)
    return "light"
    
@app.route("/light5")
def light5():
    strip.on(198)
    sleep(1)
    strip.off(198)
    return "light"
    
@app.route("/light6")
def light6():
    strip.on(195)
    sleep(1)
    strip.off(195)
    return "light"
    
@app.route("/light7")
def light7():
    strip.on(194)
    sleep(1)
    strip.off(194)
    return "light"
    
@app.route("/light8")
def light8():
    strip.on(196)
    sleep(1)
    strip.off(196)
    return "light"  

@app.route("/reds")
def lightred():
    strip.on(198)
    strip.on(195)
    strip.on(194)
    strip.on(196)
    sleep(5)
    strip.off(198)
    strip.off(195)
    strip.off(194)
    strip.off(196)
    
    
    return "light"
@app.route("/blues")
def lightblue():

    strip.on(197)
    strip.on(199)
    strip.on(193)
    strip.on(192)
    sleep(5)
    strip.off(197)
    strip.off(199)
    strip.off(193)
    strip.off(192)
    
    
    return "light"

@app.route("/lightsequence")
def lightsequence():
    strip.on(196)
    strip.on(192)
    sleep(0.1)
    strip.off(196)
    strip.off(192)
    strip.on(197)
    strip.on(194)
    sleep(0.1)
    strip.off(197)
    strip.off(194)
    strip.on(196)
    strip.on(192)
    strip.on(194)
    strip.on(195)
    sleep(0.1)
    strip.off(196)
    strip.off(192)
    strip.off(194)
    strip.off(195)
    strip.on(193)
    strip.on(197)
    strip.on(199)
    strip.on(198)
    sleep(0.1)
    strip.off(193)
    strip.off(197)
    strip.off(199)
    strip.off(198)

    strip.on(196)
    strip.on(192)
    sleep(0.1)
    strip.off(196)
    strip.off(192)
    strip.on(197)
    strip.on(194)
    sleep(0.1)
    strip.off(197)
    strip.off(194)
    strip.on(196)
    strip.on(192)
    strip.on(194)
    strip.on(195)
    sleep(0.1)
    strip.off(196)
    strip.off(192)
    strip.off(194)
    strip.off(195)
    strip.on(193)
    strip.on(197)
    strip.on(199)
    strip.on(198)
    sleep(0.1)
    strip.off(193)
    strip.off(197)
    strip.off(199)
    strip.off(198)

    strip.on(196)
    strip.on(192)
    sleep(1)
    strip.off(196)
    strip.off(192)
    strip.on(197)
    strip.on(194)
    sleep(0.1)
    strip.off(197)
    strip.off(194)
    strip.on(196)
    strip.on(192)
    strip.on(194)
    strip.on(195)
    sleep(1)
    strip.off(196)
    strip.off(192)
    strip.off(194)
    strip.off(195)
    strip.on(193)
    strip.on(197)
    strip.on(199)
    strip.on(198)
    sleep(0.1)
    strip.off(193)
    strip.off(197)
    strip.off(199)
    strip.off(198)

    strip.on(196)
    strip.on(192)
    sleep(0.1)
    strip.off(196)
    strip.off(192)
    strip.on(197)
    strip.on(194)
    sleep(0.1)
    strip.off(197)
    strip.off(194)
    strip.on(196)
    strip.on(192)
    strip.on(194)
    strip.on(195)
    sleep(0.1)
    strip.off(196)
    strip.off(192)
    strip.off(194)
    strip.off(195)
    strip.on(193)
    strip.on(197)
    strip.on(199)
    strip.on(198)
    sleep(0.1)
    strip.off(193)
    strip.off(197)
    strip.off(199)
    strip.off(198)
    
    strip.on(196)
    strip.on(192)
    sleep(0.5)
    strip.off(196)
    strip.off(192)
    strip.on(197)
    strip.on(194)
    sleep(0.5)
    strip.off(197)
    strip.off(194)
    strip.on(196)
    strip.on(192)
    strip.on(194)
    strip.on(195)
    sleep(0.5)
    strip.off(196)
    strip.off(192)
    strip.off(194)
    strip.off(195)
    strip.on(193)
    strip.on(197)
    strip.on(199)
    strip.on(198)
    sleep(0.5)
    strip.off(193)
    strip.off(197)
    strip.off(199)
    strip.off(198)
    
    strip.on(197)
    sleep(0.5)
    strip.on(199)
    sleep(0.5)
    strip.on(193)
    sleep(0.5)
    strip.on(192)
    sleep(0.5)
    strip.on(198)
    sleep(0.5)
    strip.on(195)
    sleep(0.5)
    strip.on(194)
    sleep(0.5)
    strip.on(196)
    sleep(4)
    strip.off(197)
    strip.off(199)
    strip.off(193)
    strip.off(192)
    strip.off(198)
    strip.off(195)
    strip.off(194)
    strip.off(196)

    strip.on(196)
    sleep(0.5)
    strip.on(194)
    sleep(0.5)
    strip.on(195)
    sleep(0.5)
    strip.on(198)
    sleep(0.5)
    strip.on(192)
    sleep(0.5)
    strip.on(193)
    sleep(0.5)
    strip.on(199)
    sleep(0.5)
    strip.on(197)
    sleep(3)
    strip.off(196)
    strip.off(194)
    strip.off(195)
    strip.off(198)
    strip.off(192)
    strip.off(193)
    strip.off(199)
    strip.off(197)

    strip.on(197)
    sleep(0.1)
    strip.on(199)
    sleep(0.1)
    strip.on(193)
    sleep(0.1)
    strip.on(192)
    sleep(0.1)
    strip.on(198)
    sleep(0.1)
    strip.on(195)
    sleep(0.1)
    strip.on(194)
    sleep(0.1)
    strip.on(196)
    sleep(0.1)
    strip.off(197)
    sleep(0.1)
    strip.off(199)
    sleep(0.1)
    strip.off(193)
    sleep(0.1)
    strip.off(192)
    sleep(0.1)
    strip.off(198)
    sleep(0.1)
    strip.off(195)
    sleep(0.1)
    strip.off(194)
    sleep(0.1)
    strip.off(196)

    strip.on(197)
    sleep(0.1)
    strip.on(199)
    sleep(0.1)
    strip.on(193)
    sleep(0.1)
    strip.on(192)
    sleep(0.1)
    strip.on(198)
    sleep(0.1)
    strip.on(195)
    sleep(0.1)
    strip.on(194)
    sleep(0.1)
    strip.on(196)
    sleep(0.1)
    strip.off(197)
    sleep(0.1)
    strip.off(199)
    sleep(0.1)
    strip.off(193)
    sleep(0.1)
    strip.off(192)
    sleep(0.1)
    strip.off(198)
    sleep(0.1)
    strip.off(195)
    sleep(0.1)
    strip.off(194)
    sleep(0.1)
    strip.off(196)

    strip.on(196)
    sleep(0.1)
    strip.on(194)
    sleep(0.1)
    strip.on(195)
    sleep(0.1)
    strip.on(198)
    sleep(0.1)
    strip.on(192)
    sleep(0.1)
    strip.on(193)
    sleep(0.1)
    strip.on(199)
    sleep(0.1)
    strip.on(197)
    sleep(0.1)
    strip.off(197)
    sleep(0.1)
    strip.off(199)
    sleep(0.1)
    strip.off(193)
    sleep(0.1)
    strip.off(192)
    sleep(0.1)
    strip.off(198)
    sleep(0.1)
    strip.off(195)
    sleep(0.1)
    strip.off(194)
    sleep(0.1)
    strip.off(196)

    strip.on(197)
    sleep(0.1)
    strip.on(199)
    sleep(0.1)
    strip.on(193)
    sleep(0.1)
    strip.on(192)
    sleep(0.1)
    strip.on(198)
    sleep(0.1)
    strip.on(195)
    sleep(0.1)
    strip.on(194)
    sleep(0.1)
    strip.on(196)
    sleep(0.1)
    strip.off(197)
    sleep(0.1)
    strip.off(199)
    sleep(0.1)
    strip.off(193)
    sleep(0.1)
    strip.off(192)
    sleep(0.1)
    strip.off(198)
    sleep(0.1)
    strip.off(195)
    sleep(0.1)
    strip.off(194)
    sleep(0.1)
    strip.off(196)

    strip.on(197)
    sleep(0.1)
    strip.on(199)
    sleep(0.1)
    strip.on(193)
    sleep(0.1)
    strip.on(192)
    sleep(0.1)
    strip.on(198)
    sleep(0.1)
    strip.on(195)
    sleep(0.1)
    strip.on(194)
    sleep(0.1)
    strip.on(196)
    sleep(0.1)
    strip.off(197)
    sleep(0.1)
    strip.off(199)
    sleep(0.1)
    strip.off(193)
    sleep(0.1)
    strip.off(192)
    sleep(0.1)
    strip.off(198)
    sleep(0.1)
    strip.off(195)
    sleep(0.1)
    strip.off(194)
    sleep(0.1)
    strip.off(196)

    strip.on(197)
    strip.on(199)
    strip.on(193)
    strip.on(192)
    sleep(0.1)
    strip.on(198)
    strip.on(195)
    strip.on(194)
    strip.on(196)
    sleep(0.1)
    strip.off(197)
    sleep(0.1)
    strip.off(199)
    sleep(0.1)
    strip.off(193)
    sleep(0.1)
    strip.off(192)
    sleep(0.1)
    strip.off(198)
    sleep(0.1)
    strip.off(195)
    sleep(0.1)
    strip.off(194)
    sleep(0.1)
    strip.off(196)

    strip.on(197)
    sleep(0.1)
    strip.on(199)
    sleep(0.1)
    strip.on(193)
    sleep(0.1)
    strip.on(192)
    sleep(0.1)
    strip.on(198)
    sleep(0.1)
    strip.on(195)
    sleep(0.1)
    strip.on(194)
    sleep(0.1)
    strip.on(196)
    sleep(0.1)
    strip.off(197)
    sleep(0.1)
    strip.off(199)
    sleep(0.1)
    strip.off(193)
    sleep(0.1)
    strip.off(192)
    sleep(0.1)
    strip.off(198)
    sleep(0.1)
    strip.off(195)
    sleep(0.1)
    strip.off(194)
    sleep(0.1)
    strip.off(196)

    strip.on(197)
    strip.on(199)
    strip.on(193)
    strip.on(192)
    sleep(0.5)
    strip.off(197)
    strip.off(199)
    strip.off(193)
    strip.off(192)

    strip.on(198)
    strip.on(195)
    strip.on(194)
    strip.on(196)
    sleep(0.5)
    strip.off(198)  
    strip.off(195)
    strip.off(194)
    strip.off(196)
    
    strip.on(197)
    strip.on(199)
    strip.on(193)
    strip.on(192)
    sleep(0.5)
    strip.off(197)
    strip.off(199)
    strip.off(193)
    strip.off(192)

    strip.on(198)
    strip.on(195)
    strip.on(194)
    strip.on(196)
    sleep(0.5)
    strip.off(198)  
    strip.off(195)
    strip.off(194)
    strip.off(196)
   
    strip.on(197)
    strip.on(199)
    strip.on(193)
    strip.on(192)
    sleep(0.5)
    strip.off(197)
    strip.off(199)
    strip.off(193)
    strip.off(192)

    strip.on(198)
    strip.on(195)
    strip.on(194)
    strip.on(196)
    sleep(0.5)
    strip.off(198)  
    strip.off(195)
    strip.off(194)
    strip.off(196)

    strip.on(197)
    strip.on(199)
    strip.on(193)
    strip.on(192)
    sleep(0.4)
    strip.off(197)
    strip.off(199)
    strip.off(193)
    strip.off(192)

    strip.on(198)
    strip.on(195)
    strip.on(194)
    strip.on(196)
    sleep(0.4)
    strip.off(198)  
    strip.off(195)
    strip.off(194)
    strip.off(196)

    strip.on(197)
    strip.on(199)
    strip.on(193)
    strip.on(192)
    sleep(0.3)
    strip.off(197)
    strip.off(199)
    strip.off(193)
    strip.off(192)

    strip.on(198)
    strip.on(195)
    strip.on(194)
    strip.on(196)
    sleep(0.3)
    strip.off(198)  
    strip.off(195)
    strip.off(194)
    strip.off(196)

    strip.on(197)
    strip.on(199)
    strip.on(193)
    strip.on(192)
    sleep(0.2)
    strip.off(197)
    strip.off(199)
    strip.off(193)
    strip.off(192)

    strip.on(198)
    strip.on(195)
    strip.on(194)
    strip.on(196)
    sleep(0.2)
    strip.off(198)  
    strip.off(195)
    strip.off(194)
    strip.off(196)

    strip.on(197)
    strip.on(199)
    strip.on(193)
    strip.on(192)
    sleep(0.1)
    strip.off(197)
    strip.off(199)
    strip.off(193)
    strip.off(192)

    strip.on(198)
    strip.on(195)
    strip.on(194)
    strip.on(196)
    sleep(0.1)
    strip.off(198)  
    strip.off(195)
    strip.off(194)
    strip.off(196)

    strip.on(197)
    strip.on(199)
    strip.on(193)
    strip.on(192)
    sleep(0.01)
    strip.off(197)
    strip.off(199)
    strip.off(193)
    strip.off(192)

    strip.on(198)
    strip.on(195)
    strip.on(194)
    strip.on(196)
    sleep(0.01)
    strip.off(198)  
    strip.off(195)
    strip.off(194)
    strip.off(196)

    strip.on(197)
    strip.on(199)
    strip.on(193)
    strip.on(192)
    sleep(0.01)
    strip.off(197)
    strip.off(199)
    strip.off(193)
    strip.off(192)

    strip.on(198)
    strip.on(195)
    strip.on(194)
    strip.on(196)
    sleep(0.01)
    strip.off(198)  
    strip.off(195)
    strip.off(194)
    strip.off(196)

    strip.on(197)
    strip.on(199)
    strip.on(193)
    strip.on(192)
    sleep(0.01)
    strip.off(197)
    strip.off(199)
    strip.off(193)
    strip.off(192)

    strip.on(198)
    strip.on(195)
    strip.on(194)
    strip.on(196)
    sleep(0.01)
    strip.off(198)  
    strip.off(195)
    strip.off(194)
    strip.off(196)

    strip.on(197)
    strip.on(199)
    strip.on(193)
    strip.on(192)
    sleep(0.01)
    strip.off(197)
    strip.off(199)
    strip.off(193)
    strip.off(192)

    strip.on(198)
    strip.on(195)
    strip.on(194)
    strip.on(196)
    sleep(0.01)
    strip.off(198)  
    strip.off(195)
    strip.off(194)
    strip.off(196)

    strip.on(197)
    strip.on(199)
    strip.on(193)
    strip.on(192)
    sleep(0.01)
    strip.off(197)
    strip.off(199)
    strip.off(193)
    strip.off(192)

    strip.on(198)
    strip.on(195)
    strip.on(194)
    strip.on(196)
    sleep(0.01)
    strip.off(198)  
    strip.off(195)
    strip.off(194)
    strip.off(196)

    strip.on(197)
    strip.on(199)
    strip.on(193)
    strip.on(192)
    sleep(0.01)
    strip.off(197)
    strip.off(199)
    strip.off(193)
    strip.off(192)

    strip.on(198)
    strip.on(195)
    strip.on(194)
    strip.on(196)
    sleep(0.01)
    strip.off(198)  
    strip.off(195)
    strip.off(194)
    strip.off(196)

    strip.on(197)
    strip.on(199)
    strip.on(193)
    strip.on(192)
    sleep(0.01)
    strip.off(197)
    strip.off(199)
    strip.off(193)
    strip.off(192)

    strip.on(198)
    strip.on(195)
    strip.on(194)
    strip.on(196)
    sleep(0.01)
    strip.off(198)  
    strip.off(195)
    strip.off(194)
    strip.off(196)


    strip.on(197)
    strip.on(199)
    strip.on(193)
    strip.on(192)
    sleep(0.01)
    strip.off(197)
    strip.off(199)
    strip.off(193)
    strip.off(192)

    strip.on(198)
    strip.on(195)
    strip.on(194)
    strip.on(196)
    sleep(0.01)
    strip.off(198)  
    strip.off(195)
    strip.off(194)
    strip.off(196)

    strip.on(197)
    strip.on(199)
    strip.on(193)
    strip.on(192)
    sleep(0.01)
    strip.off(197)
    strip.off(199)
    strip.off(193)
    strip.off(192)

    strip.on(198)
    strip.on(195)
    strip.on(194)
    strip.on(196)
    sleep(0.01)
    strip.off(198)  
    strip.off(195)
    strip.off(194)
    strip.off(196)
    
    strip.on(197)
    strip.on(199)
    strip.on(193)
    strip.on(192)
    sleep(0.01)
    strip.off(197)
    strip.off(199)
    strip.off(193)
    strip.off(192)

    strip.on(198)
    strip.on(195)
    strip.on(194)
    strip.on(196)
    sleep(0.01)
    strip.off(198)  
    strip.off(195)
    strip.off(194)
    strip.off(196)

    strip.on(197)
    strip.on(199)
    strip.on(193)
    strip.on(192)
    sleep(0.05)
    strip.off(197)
    strip.off(199)
    strip.off(193)
    strip.off(192)

    strip.on(198)
    strip.on(195)
    strip.on(194)
    strip.on(196)
    sleep(0.05)
    strip.off(198)  
    strip.off(195)
    strip.off(194)
    strip.off(196)

    strip.on(197)
    strip.on(199)
    strip.on(193)
    strip.on(192)
    sleep(0.05)
    strip.off(197)
    strip.off(199)
    strip.off(193)
    strip.off(192)

    strip.on(198)
    strip.on(195)
    strip.on(194)
    strip.on(196)
    sleep(0.05)
    strip.off(198)  
    strip.off(195)
    strip.off(194)
    strip.off(196)


    strip.on(197)
    strip.on(199)
    strip.on(193)
    strip.on(192)
    sleep(0.05)
    strip.off(197)
    strip.off(199)
    strip.off(193)
    strip.off(192)

    strip.on(198)
    strip.on(195)
    strip.on(194)
    strip.on(196)
    sleep(0.05)
    strip.off(198)  
    strip.off(195)
    strip.off(194)
    strip.off(196)

    strip.on(197)
    strip.on(199)
    strip.on(193)
    strip.on(192)
    sleep(0.05)
    strip.off(197)
    strip.off(199)
    strip.off(193)
    strip.off(192)

    strip.on(198)
    strip.on(195)
    strip.on(194)
    strip.on(196)
    sleep(0.05)
    strip.off(198)  
    strip.off(195)
    strip.off(194)
    strip.off(196)
    

    return "light" 
            
@app.route('/camera')
def index():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH,320);
    cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT,240);
    def camera():
        while True:
            rval, frame = cap.read()
            ret, jpeg = cv2.imencode('.jpg', frame, (cv2.IMWRITE_JPEG_QUALITY, 20))
            yield b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + jpeg.tostring() + b'\r\n\r\n' 
    return Response(camera(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/api/wireless", methods=['GET', 'POST'])
def wireless():
    networks = []
    #if request.method == 'POST':
        #print (request.form)
    #Getting the information about the network
    for dev in NetworkManager.NetworkManager.GetDevices():
        if dev.DeviceType != NetworkManager.NM_DEVICE_TYPE_WIFI:
            continue
    for ap in dev.SpecificDevice().GetAccessPoints():
        networks.append({"ssid":ap.Ssid, "freq":ap.Frequency, "strength":ord(ap.Strength)})
    #for perm, val in sorted(NetworkManager.NetworkManager.GetPermissions().items()):
        return json.dumps(networks)



@app.route("/css.css")
def css():
    return app.send_static_file('css.css')
    
@app.route("/app.js")
def java():
    return app.send_static_file('app.js')

@app.route("/")
def robot():
    return app.send_static_file('robot.html')

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
    
#Chaning the port and host and the debug from the command line 
if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option("-H", "--host",
        help="Bind to address, default to all interfaces",
        default="0.0.0.0")
    parser.add_option("-P", "--port",
        type=int,
        help="Listen on this port, default to 5000",
        default=5000)
    parser.add_option("-d", "--debug",
        action="store_true", dest="debug",
        help=optparse.SUPPRESS_HELP)
    options, _ = parser.parse_args()

    app.run(
        debug=options.debug,
        host=options.host,
        port=options.port
    )


