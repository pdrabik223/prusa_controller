from dataclasses import dataclass
import dataclasses
import time
from flask import Flask, json, render_template, request
from flask_socketio import SocketIO, emit
from serial import SerialException

from controller import prusa_device

app = Flask(__name__)
socketio = SocketIO(app)


@dataclass
class PrinterStatus:
    is_connected: bool = False
    is_busy: bool = False
    position: tuple[float, float, float] | None
    current_task: str | None

    def to_dict(self):
        return {
            "is_connected": self.is_connected,
            "position": self.position,
            "is_busy": self.is_busy,
            "current_task": self.current_task,
        }


# TODO here we might have thread collisions
prusa_controller: prusa_device.PrusaDevice = None
log_queue: list[str] = []
prusa_status: PrinterStatus = PrinterStatus()


def connect_to_printer():
    global prusa_controller
    global prusa_status

    prusa_status = PrinterStatus(is_busy=True, current_task="startup_procedure")

    if prusa_controller != None:
        del prusa_controller
        prusa_controller = None

    try:
        prusa_controller = prusa_device.PrusaDevice.connect()
    except SerialException as ex:
        print("Serial error")
        prusa_status = PrinterStatus(is_connected=False)
        log_queue.append("Connection to printer failed")
        return

    time.sleep(5)
    prusa_controller.startup_procedure()
    time.sleep(5)

    prusa_controller.send_and_await("G28 W")
    prusa_controller.send_and_await("G1 X0 Y0 Z10")
    prusa_status = PrinterStatus(is_connected=True, position=[0, 0, 10])

@socketio.on("connect")
def test_connect(auth):
    emit("connect", {"data": "connected"})
    send_status()


@socketio.on("disconnect")
def test_disconnect(reason):
    print("Client disconnected, reason:", reason)


@socketio.on("gcode")
def handle_my_custom_event(json):
    print("received json: " + str(json))


def send_status(current: PrinterStatus):
    emit("status", {"status": json.dumps(dataclasses.asdict(current))})


def log_command(info: list[str]):
    emit("log", {"messages": info})


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/connect_to_printer", methods=["GET"])
def connect_to_printer_endpoint():
    global prusa_controller
    if prusa_controller == None:
        connect_to_printer()

    return "ok", 200


@app.route("/gcode", methods=["POST"])
def handleGcode():
    global prusa_controller
    if prusa_controller == None:
        return "connect to printer", 500
    #     connect_to_printer()
    # emit connect to printer stuff
    commands = request.get_json()["gcode"]
    prusa_controller.send_and_await(commands)
    return "ok"


if __name__ == "__main__":
    socketio.run(app, debug=True)
