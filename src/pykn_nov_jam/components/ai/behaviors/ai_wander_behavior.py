import pykraken as kn

from pykn_nov_jam.components.ai.ai_input_data import AiInputData
from pykn_nov_jam.components.ai.behaviors.ai_behavior import AiBehavior
from pykn_nov_jam.entities.entity import Entity


class AiWanderBehavior(AiBehavior):
    def __init__(
        self, entity: Entity, priority: int, wander_radius: float = 50.0
    ) -> None:
        super().__init__(entity, priority)
        self.wander_radius: float = wander_radius

    def evaluate_behavior(self, delta_time: float, input_data: AiInputData) -> float:
        if input_data.fear_level < 0.6:
            # print(f"\tFear Level: {input_data.fear_level}")
            return 0.6
        return 0.2

    def get_steering_vector(self, input_data: AiInputData) -> kn.Vec2:
        return (
            self.steering.wander(self.wander_radius) if self.steering else kn.Vec2(0, 0)
        )
