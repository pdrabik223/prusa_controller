import enum
import time
from serial import Serial
from serial import SerialException
from typing import Optional
import serial.tools.list_ports


import time

from typing import Optional, Tuple

import serial.tools.list_ports
import enum
from typing import Optional, Tuple


def list_available_serial_ports():
    ports = serial.tools.list_ports.comports()
    for port, desc, hwid in sorted(ports):
        print("{}: {} [{}]".format(port, desc, hwid))


class Point3D:
    def __init__(self, x=0, y=0, z=0):
        self.x: Optional[float] = x
        self.y: Optional[float] = y
        self.z: Optional[float] = z

    def is_none(self):
        return self.x is None or self.y is None or self.z is None

    def from_tuple(self, position: Tuple[float, float, float]):
        self.x = position[0]
        self.y = position[1]
        self.z = position[2]

    def as_tuple(self) -> Optional[Tuple[float, float, float]]:
        return self.x, self.y, self.z


class PrusaDevice:
    _device: Serial = None  # pyserial connector device

    def __init__(self, device) -> None:
        super().__init__()
        self._device = device

    # TODO READ on self
    def __del__(self) -> None:
        if self._device is None:
            return

        commands = [
            "G4",  # wait
            "M221 S100",  # reset flow
            "M900 K0",  # reset LA
            "M907 E538",  # reset extruder motor current
            "M104 S0",  # turn off temperature
            "M140 S0",  # turn off heated
            "M107 M84",  # turn off fan  # disable motors
        ]
        for command in commands:
            self.send_and_await(command=command)

        self._device.close()

    @staticmethod
    def connect_on_port(port: str, baudrate: int = 115200, timeout=2) -> "PrusaDevice":
        """
        Connect to Prusa device
        Args:
            port (str): COM port on windows system, usually 9.
            baudrate (int, optional): baudrate. Defaults to 115200.
            timeout (int, optional): timeout. Defaults to 5.

        Returns:
            PrusaDevice: _description_
        """
        device = Serial(port=port, baudrate=baudrate, timeout=timeout)
        time.sleep(2)

        resp = device.readline().decode("utf-8")

        while resp != "":
            print(resp.strip())
            resp = device.readline().decode("utf-8")

        return PrusaDevice(device)

    @staticmethod
    def connect() -> "PrusaDevice":
        baudrate: int = 115200
        timeout: int = 1
        device: Optional[Serial] = None
        available_ports = sorted(serial.tools.list_ports.comports())

        print("Available ports:")
        for port, desc, hwid in available_ports:
            print(f"\t port: '{port}', desc: '{desc}', hwid: '{hwid}")

        for port, desc, _ in available_ports:
            print(f"Scanning port: '{port}', desc: '{desc}'")
            try:
                device: Serial = Serial(
                    port=str(port), baudrate=baudrate, timeout=timeout
                )

                print(f"Serial port is Open'")
                time.sleep(1)

                if "start" not in device.readline().decode("utf-8"):
                    print("Failed to connect to prusa device")
                    raise SerialException()

                print(f"Connected on port: '{port}', desc: '{desc}'")
                break

            except SerialException:
                device = None
                continue

        if not device:
            raise SerialException("Device not found")

        resp = device.readline().decode("utf-8")
        while resp != "":
            print(resp.strip())
            resp = device.readline().decode("utf-8")

        return PrusaDevice(device=device)

    class PrusaPrinterStatus(enum.Enum):
        PROCESSING = "processing"
        READY = "ready"

    def send_and_await(self, command: str) -> str:
        command = command.strip()

        if command[-1] != "\r":
            command += "\r"

        if command[-1] != "\n":
            command += "\n"

        self._device.write(bytearray(command, "utf-8"))
        # self._device.write(bytearray("M400\r\n", "utf-8"))

        resp = ""
        retries = 5
        r = 0

        # after every successfully completed command, prusa returns 'ok' message
        while "ok" not in resp:
            resp = str(self._device.readline().decode("utf-8"))

            if "busy" in resp:
                print("awaiting 0.25s")
                time.sleep(0.25)

            elif "Command not found!" in resp:
                print('"', command, '"')
                break

            # add a case for cache rilled up
            else:
                r += 1
                time.sleep(0.1)
                if r > retries:
                    return "none message"

    def startup_procedure(self) -> None:
        """
        send default parameters (motor speed, acceleration, model check, etc...)
        this header is working, but not verified
        """

        commands = [
            "; generated by PrusaSlicer 2.7.4+win64 on 2025-11-16 at 11:48:13 UTC",
            "; external perimeters extrusion width = 0.45mm",
            "; perimeters extrusion width = 0.45mm",
            "; infill extrusion width = 0.45mm",
            "; solid infill extrusion width = 0.45mm",
            "; top infill extrusion width = 0.40mm",
            "; first layer extrusion width = 0.42mm",
            "M73 P0 R0",
            "M73 Q0 S0",
            "M201 X1000 Y1000 Z200 E5000 ; sets maximum accelerations, mm/sec^2",
            "M203 X200 Y200 Z12 E120 ; sets maximum feedrates, mm / sec",
            "M204 S1250 T1250 ; sets acceleration (S) and retract acceleration (R), mm/sec^2",
            "M205 X8.00 Y8.00 Z0.40 E4.50 ; sets the jerk limits, mm/sec",
            "M205 S0 T0 ; sets the minimum extruding and travel feed rate, mm/sec",
        ]

        for command in commands:
            self.send_and_await(command=command)
