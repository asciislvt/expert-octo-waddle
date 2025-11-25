import math
import random

import pykraken as kn

from pykn_nov_jam.components.key_input_component import InputComponent
from pykn_nov_jam.components.movement_component import MovementComponent
from pykn_nov_jam.entities.entity import Entity


class AiSteeringComponent(InputComponent):
    def __init__(
        self,
        entity: Entity,
        fleeing: bool = False,
    ) -> None:
        super().__init__(entity)
        self.fleeing: bool = fleeing
        self.wander_angle: float = 0.0

    # def process_draw(self) -> None:
    #     debug_input_line = kn.Line(
    #         self.entity.position, self.input_direction * 32 + self.entity.position
    #     )
    #     debug_input_line_color = kn.color.GREEN
    #     kn.draw.line(debug_input_line, debug_input_line_color, 2)

    def seek(self, target_pos: kn.Vec2, flee: bool = False) -> kn.Vec2:
        movement_component: MovementComponent = self.entity.get_component(
            MovementComponent
        )  # type: ignore
        dir_to_target = kn.Vec2(0, 0)

        if flee:
            dir_to_target = self.entity.position - target_pos
        else:
            dir_to_target = target_pos - self.entity.position
        dir_to_target.normalize()

        wish_velocity = dir_to_target * movement_component.max_speed
        steer_velocity = wish_velocity - movement_component.velocity

        steer_velocity.normalize()
        return steer_velocity

    def wander(self, wander_radius: float) -> kn.Vec2:
        movement_component: MovementComponent = self.entity.get_component(
            MovementComponent
        )  # type: ignore
        steering = kn.Vec2(0, 0)
        self.wander_angle += random.uniform(-0.2, 0.2)

        wander_circle = self.entity.position + movement_component.velocity
        wander_point = kn.Vec2(
            wander_circle.x + wander_radius * math.cos(self.wander_angle),
            wander_circle.y + wander_radius * math.sin(self.wander_angle),
        )

        steering = (wander_point - self.entity.position) * movement_component.max_speed
        steering.normalize()
        return steering
