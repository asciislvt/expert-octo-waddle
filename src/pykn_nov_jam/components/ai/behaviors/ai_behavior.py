import pykraken as kn

from pykn_nov_jam.components.ai.ai_input_data import AiInputData
from pykn_nov_jam.components.ai.ai_steering_component import AiSteeringComponent
from pykn_nov_jam.components.component import Component
from pykn_nov_jam.entities.entity import Entity


class AiBehavior(Component):
    def __init__(
        self, entity: Entity, priority: int, is_exclusive: bool = False
    ) -> None:
        super().__init__(entity)
        self.priority: int = priority
        self.weight: float = 0.0
        self.steering: AiSteeringComponent | None = entity.get_component(
            AiSteeringComponent
        )  # type: ignore
        self.is_exclusive: bool = is_exclusive

    def evaluate_behavior(self, delta_time: float, input_data: AiInputData) -> float:
        return 0.0

    def get_steering_vector(self, input_data: AiInputData) -> kn.Vec2:
        return kn.Vec2(0, 0)
