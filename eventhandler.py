from threading import Thread


class Eventhandler(object):
    def __init__(self, carcontroller) -> None:
        super().__init__()
        self.carcontroller = carcontroller
        self.prev_state = {**self.carcontroller.data}
        self.current_state = {**self.carcontroller.data}
        self.actions = []
        self.changed = False

    def handle_events(self):
        while not self.carcontroller.data["DONE"]:
            for key in self.current_state:
                if self.prev_state[key] != self.current_state[key]:
                    # print(key, self.prev_state[key], self.current_state[key])
                    # print(key, self.prev_state[key], self.current_state[key])
                    e = Event(value=self.current_state[key])
                    if key == "L_Y":
                        self.changed = True
                        e.type = EventType.THROTTLE

                    self.actions.append(e)
            self.prev_state = self.current_state.copy()
            self.current_state = {**self.carcontroller.data}
            if self.changed:
                self.changed = False
                self.action_thread = Thread(
                    target=self.handle_actions, kwargs={"actions": self.actions.copy()}
                )
                self.action_thread.start()
            self.actions = []

    def handle_actions(self, **kwargs):
        actions = kwargs.get("actions")
        for action in actions:
            if action.type == EventType.THROTTLE:
                self.carcontroller.motorcontroller.throttle(action.value)

    def steer_left(self, value):
        pass

    def steer_right(self, value):
        pass

    def refresh_controller(self):
        pass

    def change_controllermode(self):
        pass


class Event:
    def __init__(self, **kwargs) -> None:
        self.value = kwargs.get("value")
        self.type = kwargs.get("type")


class EventType:
    STEER = 0
    THROTTLE = 1
    BRAKE = 2
    PULL = 8
    PULL = 8
