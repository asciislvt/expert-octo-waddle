import pykraken as kn
from pykn_nov_jam.components.component import Component
from pykn_nov_jam.globals import Globals


class WhistleComponent(Component):
    def __init__(self, entity) -> None:
        super().__init__(entity)
        self.is_whistling: bool = False

    def process_input(self) -> None:
        if Globals._instance is None:
            return

        if kn.key.is_just_pressed(kn.K_LSHIFT):
            self.is_whistling = True
            print("Player is whistling")
        if kn.key.is_just_released(kn.K_LSHIFT):
            self.is_whistling = False
            print("Player stopped whistling")
