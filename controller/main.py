import time
import serial
import sys
import glob
import serial

from pad_cotrol import Controller
from prusa_device import PrusaDevice
pad = Controller()
prusa = PrusaDevice.connect()


time.sleep(5)
prusa.startup_procedure()
time.sleep(5)


prusa.send_and_await("G28 W")
prusa.send_and_await("G1 Z10")
resp = input("""[1] enable manual control
[2] pad control
[q] quit""")

current_position = (0,0,10)
if resp.strip() == '2':
    step = 0.1
    
    while True:
        [x, y, up, down] = pad.read()
        x = current_position[0] + step * x
        y = current_position[1] + step * y
        z = current_position[2]
        
        if (up != 0):
            z = current_position[2] + step
        
        if (down != 0):
            z = current_position[2] - step
        
        
        if x < 0 or x > 200:
            x =  current_position[0]
            
        if y < 0 or y > 200:
            y =  current_position[1]
            
        if z < 0 or z > 200:
            z =  current_position[2]
        
        x = round(x,2)
        y = round(y,2)
        z = round(z,2)
        
        if(x != current_position[0] or y != current_position[1] or z != current_position[2]):
            current_position = (x,y,z)
            new_gcode = f"G1 X{x} Y{y} Z{z}"
            prusa.send_and_await(new_gcode)
            print(new_gcode)
            # time.sleep(0.1)

elif resp.strip() == '1':

    x = ""
    while x != 'q':
        x = input("Send command to 3d printer")
        prusa.send_and_await(x)
