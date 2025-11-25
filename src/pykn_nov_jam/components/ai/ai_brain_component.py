import pykraken as kn

import random
from pykn_nov_jam.components.ai.ai_input_data import AiInputData
from pykn_nov_jam.components.ai.ai_steering_component import AiSteeringComponent
from pykn_nov_jam.components.component import Component
from pykn_nov_jam.entities.entity import Entity


class AiBrainComponent(Component):
    def __init__(self, entity: Entity) -> None:
        super().__init__(entity)
        self.steering: AiSteeringComponent = entity.get_component(AiSteeringComponent)  # type: ignore
        self.input_data: AiInputData = AiInputData()

    def set_input_data(self, input_data: AiInputData) -> None:
        self.input_data = input_data

    def process_update(self, delta_time: float) -> None:
        if self.enabled is False:
            return

        if self.input_data.whistle:
            steering_vector = self.steering.seek(self.input_data.player_position)
            if steering_vector.length > 0:
                self.steering.input_direction = steering_vector
        else:
            # regular wandering behavior
            wander_radius = 50.0
            steering_vector = self.steering.wander(wander_radius)
            if steering_vector.length > 0:
                self.steering.input_direction = steering_vector
