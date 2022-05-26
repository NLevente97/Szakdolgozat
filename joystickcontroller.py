from pyPS4Controller.controller import Controller


class JoystickController(Controller):
    def __init__(self, **kwargs) -> None:
        self.motorcontroller = kwargs["motorcontroller"]
        kwargs.pop("motorcontroller")
        Controller.__init__(self, **kwargs)
        self.capacity = -1

    def start(self):
        self.listen(
            timeout=60, on_connect=self.connected, on_disconnect=self.disconnected
        )

    def connected(self):
        pass

    def disconnected(self):
        pass

    # L_Y
    def on_L3_left(self, value):
        self.motorcontroller.carcontroller.data["L_X"] = value / 32767
        # self.motorcontroller.servocontroller.steer(
        #    self.motorcontroller.data["L_X"])

    def on_L3_right(self, value):
        self.motorcontroller.carcontroller.data["L_X"] = value / 32767
        # self.motorcontroller.eventhandler.steer()

    def on_L3_x_at_rest(self):
        self.motorcontroller.carcontroller.data["L_X"] = 0
        # self.motorcontroller.servocontroller.steer_reset()

    def on_L3_up(self, value):
        self.motorcontroller.carcontroller.data["L_Y"] = value / 32767

    def on_L3_down(self, value):
        self.motorcontroller.carcontroller.data["L_Y"] = value / 32767

    def on_L3_y_at_rest(self):
        self.motorcontroller.carcontroller.data["L_Y"] = 0

    # SHARE
    def on_share_press(self):
        self.motorcontroller.carcontroller.data["SHARE"] = 1
        #print("exiting program")
        self.motorcontroller.reset()

    def on_share_release(self):
        self.motorcontroller.carcontroller.data["SHARE"] = 0
        self.motorcontroller.carcontroller.data["DONE"] = True
        
