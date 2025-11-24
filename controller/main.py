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
resp = input(
    """[1] enable manual control
[2] pad control
[q] quit\n  """
)

current_position = (0, 0, 10)
if resp.strip() == "2":
    
    step = 0.1
    horizontal_step = 0.5
    
    max_speed = 1000
    min_speed = 100
    movement_speed = 100
    
    while True:
        # time.sleep(0.1)
        [x, y, up, down, speed] = [
            round(pad.LeftJoystickX,2),
            round(pad.LeftJoystickY,2),
            pad.RightBumper,
            pad.LeftBumper,
            round(pad.RightTrigger,2)
        ]

        x = current_position[0] + x * (horizontal_step * speed * 10)
        y = current_position[1] + y * (horizontal_step * speed * 10)
        z = current_position[2]
        
        speed = speed * max_speed
        
        if speed < min_speed:
            speed = min_speed
        elif speed > max_speed:
            speed = max_speed
            
        if up != 0:
            z = current_position[2] + step

        if down != 0:
            z = current_position[2] - step

        if x < 0 or x > 200:
            x = current_position[0]

        if y < 0 or y > 200:
            y = current_position[1]

        if z < 0 or z > 200:
            z = current_position[2]

        x = round(x, 3)
        y = round(y, 3)
        z = round(z, 3)
        speed = round(speed)
        
        
        if (
            speed != 0
            and (x != current_position[0]
            or y != current_position[1]
            or z != current_position[2])
        ):
            current_position = (x, y, z)
            
            new_gcode = f"G1 X{x} Y{y} Z{z} F{speed}"
            
            prusa.send_and_await(new_gcode)
            print(new_gcode)
            # time.sleep(0.1)

elif resp.strip() == "1":

    x = ""
    while x != "q":
        x = input("Send command to 3d printer")
        prusa.send_and_await(x)
