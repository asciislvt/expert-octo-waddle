import pykraken as kn
from pykn_nov_jam.components.component import Component
from pykn_nov_jam.globals import Globals


class WhistleComponent(Component):
    def __init__(self, entity) -> None:
        super().__init__(entity)

    def process_input(self) -> None:
        if Globals._instance is None:
            return

        if kn.key.is_pressed(kn.K_LSHIFT):
            Globals._instance.player_is_whistling = True
            print("Player is whistling")
        else:
            Globals._instance.player_is_whistling = False
