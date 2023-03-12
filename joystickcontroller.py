# a custom made library for the Playstation 4 controller
# found at https://github.com/ArturSpirin/pyPS4Controller
from pyPS4Controller.controller import Controller

# the class that is used to handle the events from the controller
class JoystickController(Controller):
    def __init__(self, **kwargs) -> None:
        # reference to the motorcontroller that is passed through the keyword arguments
        self.motorcontroller = kwargs["motorcontroller"]
        # popping the motorcontroller from the keyword arguments,
        # so that they can be used to initialize the Playstation4 controller
        kwargs.pop("motorcontroller")
        Controller.__init__(self, **kwargs)
        # the battery level of the controller (currently unused)
        self.capacity = -1

    # the function that is called to await for the connection of the controller
    def start(self):
        self.listen(
            timeout=60, on_connect=self.connected, on_disconnect=self.disconnected
        )

    # the callback function that is called when the controller is connected
    def connected(self):
        pass

    # the callback function that is called when the controller is disconnected
    def disconnected(self):
        pass

    # functions for the left joystick
    # normalizing the value to be between 0 and 1

    # L_X
    def on_L3_left(self, value):
        self.motorcontroller.robotcontroller.data["L"] = (
            self.motorcontroller.robotcontroller.data["L"][0],
            value / 32767,
        )
        print(f"left {value}")

    def on_L3_right(self, value):
        self.motorcontroller.robotcontroller.data["L"] = (
            self.motorcontroller.robotcontroller.data["L"][0],
            value / 32767,
        )
        print(f"right {value}")

    def on_L3_x_at_rest(self):
        self.motorcontroller.robotcontroller.data["L"] = (
            self.motorcontroller.robotcontroller.data["L"][0],
            0,
        )

    # L_Y
    def on_L3_up(self, value):
        self.motorcontroller.robotcontroller.data["L"] = (
            value / 32767,
            self.motorcontroller.robotcontroller.data["L"][1],
        )

    def on_L3_down(self, value):
        self.motorcontroller.robotcontroller.data["L"] = (
            value / 32767,
            self.motorcontroller.robotcontroller.data["L"][1],
        )

    def on_L3_y_at_rest(self):
        self.motorcontroller.robotcontroller.data["L"] = (
            0,
            self.motorcontroller.robotcontroller.data["L"][1],
        )

    # functions for the "share" button, that is used to exit the program
    # SHARE
    def on_share_press(self):
        self.motorcontroller.robotcontroller.data["SHARE"] = 1
        # print("exiting program")
        self.motorcontroller.reset()

    def on_share_release(self):
        self.motorcontroller.robotcontroller.data["SHARE"] = 0
        self.motorcontroller.robotcontroller.data["DONE"] = True

    # R2, "handbrake"
    def on_R2_press(self, value):
        self.motorcontroller.robotcontroller.data["Brake"] = True

    def on_R2_release(self):
        self.motorcontroller.robotcontroller.data["Brake"] = False
