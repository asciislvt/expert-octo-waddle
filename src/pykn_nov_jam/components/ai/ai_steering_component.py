import math
import random

import pykraken as kn

from pykn_nov_jam.components.key_input_component import InputComponent
from pykn_nov_jam.components.movement_component import MovementComponent
from pykn_nov_jam.entities.entity import Entity
from pykn_nov_jam.globals import Globals


class AiSteeringComponent(InputComponent):
    def __init__(
        self,
        entity: Entity,
        fleeing: bool = False,
    ) -> None:
        super().__init__(entity)
        self.fleeing: bool = fleeing
        self.wander_angle: float = 0.0
        # self.motion_component: MovementComponent = self.entity.get_component(  # type: ignore
        #     MovementComponent
        # )
        self.target_position: kn.Vec2 = kn.Vec2(0, 0)

    def set_target_position(self, target_pos: kn.Vec2) -> None:
        self.target_position = target_pos

    def process_input(self) -> None:
        pass
        # steering = self.seek(self.target_position)
        # self.input_direction = steering

    def process_draw(self) -> None:
        debug_input_line = kn.Line(
            self.entity.position, self.input_direction * 32 + self.entity.position
        )
        debug_input_line_color = kn.color.GREEN
        kn.draw.line(debug_input_line, debug_input_line_color, 2)

    def seek(self, target_pos: kn.Vec2, flee: bool = False) -> kn.Vec2:
        movement_component: MovementComponent = self.entity.get_component(
            MovementComponent
        )  # type: ignore
        dir_to_target = kn.Vec2(0, 0)

        if flee:
            dir_to_target = self.entity.position - target_pos
        else:
            dir_to_target = self.target_position - target_pos
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
        # self.wander_angle = self.wander_angle % (2 * math.pi)
        # print(self.wander_angle)

        wander_circle = self.entity.position + movement_component.velocity
        wander_point = kn.Vec2(
            wander_circle.x + wander_radius * math.cos(self.wander_angle),
            wander_circle.y + wander_radius * math.sin(self.wander_angle),
        )

        steering = (wander_point - self.entity.position) * movement_component.max_speed
        steering.normalize()
        return steering
