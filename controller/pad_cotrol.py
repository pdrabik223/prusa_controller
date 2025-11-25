import time
from inputs import get_gamepad
import math
import threading


class Controller:
    MAX_TRIG_VAL = math.pow(2, 8)
    MAX_JOY_VAL = math.pow(2, 15)

    def __init__(self):

        self.LeftJoystickY = 0
        self.LeftJoystickX = 0
        self.RightJoystickY = 0
        self.RightJoystickX = 0
        self.LeftTrigger = 0
        self.RightTrigger = 0
        self.LeftBumper = 0
        self.RightBumper = 0
        self.A = 0
        self.X = 0
        self.Y = 0
        self.B = 0
        self.LeftThumb = 0
        self.RightThumb = 0
        self.Back = 0
        self.Start = 0
        self.LeftDPad = 0
        self.RightDPad = 0
        self.UpDPad = 0
        self.DownDPad = 0

        self._monitor_thread = threading.Thread(
            target=self._monitor_controller, args=()
        )
        self._monitor_thread.daemon = True
        self._monitor_thread.start()



    def _monitor_controller(self):
        while True:

            events = get_gamepad()
            for event in events:
                if event.code == "ABS_Y":
                    self.LeftJoystickY = (
                        event.state / Controller.MAX_JOY_VAL
                    )  # normalize between -1 and 1
                elif event.code == "ABS_X":
                    self.LeftJoystickX = (
                        event.state / Controller.MAX_JOY_VAL
                    )  # normalize between -1 and 1
                elif event.code == "ABS_RY":
                    self.RightJoystickY = (
                        event.state / Controller.MAX_JOY_VAL
                    )  # normalize between -1 and 1
                elif event.code == "ABS_RX":
                    self.RightJoystickX = (
                        event.state / Controller.MAX_JOY_VAL
                    )  # normalize between -1 and 1
                elif event.code == "ABS_Z":
                    self.LeftTrigger = (
                        event.state / Controller.MAX_TRIG_VAL
                    )  # normalize between 0 and 1
                elif event.code == "ABS_RZ":
                    self.RightTrigger = (
                        event.state / Controller.MAX_TRIG_VAL
                    )  # normalize between 0 and 1
                elif event.code == "BTN_TL":
                    self.LeftBumper = event.state
                elif event.code == "BTN_TR":
                    self.RightBumper = event.state
                elif event.code == "BTN_SOUTH":
                    self.A = event.state
                elif event.code == "BTN_NORTH":
                    self.Y = event.state  # previously switched with X
                elif event.code == "BTN_WEST":
                    self.X = event.state  # previously switched with Y
                elif event.code == "BTN_EAST":
                    self.B = event.state
                elif event.code == "BTN_THUMBL":
                    self.LeftThumb = event.state
                elif event.code == "BTN_THUMBR":
                    self.RightThumb = event.state
                elif event.code == "BTN_SELECT":
                    self.Back = event.state
                elif event.code == "BTN_START":
                    self.Start = event.state
                elif event.code == "BTN_TRIGGER_HAPPY1":
                    self.LeftDPad = event.state
                elif event.code == "BTN_TRIGGER_HAPPY2":
                    self.RightDPad = event.state
                elif event.code == "BTN_TRIGGER_HAPPY3":
                    self.UpDPad = event.state
                elif event.code == "BTN_TRIGGER_HAPPY4":
                    self.DownDPad = event.state

def increase_speed(speed, increase_amount, default_values = {"speed_increase_frames" : 1000, "max_speed" : 500, "min_speed" : 0}):
    
    increase_per_frame = (default_values["max_speed"] - default_values["min_speed"]) / default_values["speed_increase_frames"]
    
    def sanitize_output(val, increase_amount, default_values = default_values):
        val = round(val, 3)
        if (val < default_values["min_speed"]): return default_values["min_speed"]
        if (val > default_values["max_speed"]): return default_values["max_speed"] * increase_amount
        return val
    
    if (increase_amount == 0):
        result =  speed - increase_per_frame
        return sanitize_output(result, increase_amount)
    
    result = speed + increase_per_frame
    return sanitize_output(result, increase_amount)
    
    

if __name__ == "__main__":
    try:
        joy = Controller()
    except Exception as ex:
        print("no pad detected")
        exit(1)
        
    speed = 0
    previous = []
    current = []
    while True:
        current = [
            round(joy.LeftJoystickX,3),
            round(joy.LeftJoystickY,3),
            joy.RightBumper,
            joy.LeftBumper,
            round(joy.RightTrigger,3)
        ]   
        speed = increase_speed(speed=speed, increase_amount=current[4])
        current[4] = speed

        if previous != current:
            print(current)
            previous = current
        
