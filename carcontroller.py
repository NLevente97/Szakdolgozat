from motorcontroller import MotorController
from joystickcontroller import JoystickController
from threading import Thread
from eventhandler import Eventhandler


class CarController(object):
    def __init__(self, **kwargs) -> None:
        super().__init__()
        self.data = {
            "L_Y": 0,
            "L_X": 0,
            "SHARE": 0,
            "DONE": False,
        }
        self.eventhandler = Eventhandler(self)
        self.motorcontroller = MotorController(carcontroller=self)
        self.joystickcontroller = JoystickController(
            interface="/dev/input/js0",
            connecting_using_ds4drv=False,
            motorcontroller=self.motorcontroller,
        )
        self.threads = []
        self.start()

    def start(self):
        joy_thread = Thread(target=self.joystickcontroller.start, daemon=True)
        joy_thread.start()
        event_thread = Thread(target=self.eventhandler.handle_events, daemon=True)
        event_thread.start()
        while not self.data["DONE"]:
            pass


if __name__ == "__main__":
    cc = CarController()
    cc.start()
