from motorcontroller import MotorController
from joystickcontroller import JoystickController
from threading import Thread
from eventhandler import Eventhandler


# main class for the robotcontroller
class RobotController(object):

    # initialize the robot controller
    def __init__(self, **kwargs) -> None:
        super().__init__()

        # the joystick data that are currently being used
        self.data = {
            "L_Y": 0,
            "L_X": 0,
            "SHARE": 0,
            "DONE": False,
            "Brake": False,
        }
        # creating the controllers for the motors and the joystick and the event handler
        self.eventhandler = Eventhandler(robotcontroller=self)
        self.motorcontroller = MotorController(robotcontroller=self)
        self.joystickcontroller = JoystickController(
            interface="/dev/input/js0",
            connecting_using_ds4drv=False,
            motorcontroller=self.motorcontroller,
        )

    # the function that is called when the robot is started
    def start(self) -> None:
        # creating threads for the joystick and the event handler and starting them
        joy_thread = Thread(target=self.joystickcontroller.start, daemon=True)
        joy_thread.start()
        event_thread = Thread(target=self.eventhandler.handle_events, daemon=True)
        event_thread.start()

        # the infinite loop that is keeping alive the other daemon threads
        while not self.data["DONE"]:
            pass


# the main function that is called when the program is started
if __name__ == "__main__":
    robotcontroller = RobotController()
    robotcontroller.start()
