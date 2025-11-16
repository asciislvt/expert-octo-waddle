from typing import override

from pykraken import Vec2

from pykn_nov_jam.components.component import Component
from pykn_nov_jam.components.key_input_component import InputComponent
from pykn_nov_jam.entities.entity import Entity


class MovementComponent(Component):
    def __init__(
        self, entity: Entity, accel: float, decel: float, max_speed: float
    ) -> None:
        super().__init__(entity)
        self.entity: Entity = entity
        self.velocity: Vec2 = Vec2(0, 0)
        self.prev_velocity: Vec2 = Vec2(0, 0)
        self.prev_position: Vec2 = entity.position.copy()
        self.accel: float = accel
        self.decel: float = decel
        self.max_speed: float = max_speed

    def get_speed(self) -> float:
        return self.velocity.length

    def get_position_delta(self) -> Vec2:
        return self.entity.position - self.prev_position

    @override
    def process_update(self, delta_time: float) -> None:
        if self.enabled is False:
            return

        self.prev_position = self.entity.position.copy()
        self.prev_velocity = self.velocity.copy()
        self.velocity -= self.velocity * self.decel * delta_time

        input_component: InputComponent | None = self.entity.get_component(
            InputComponent
        )  # pyright: ignore[reportAssignmentType]

        if input_component is None:
            print("No InputComponent found in MovementComponent")
            return

        wish_speed = input_component.input_direction.length * self.max_speed
        self.accelerate(input_component.input_direction, wish_speed, delta_time)

        self.entity.position += self.velocity * delta_time

    def accelerate(self, wish_dir: Vec2, wish_speed: float, delta_time: float) -> None:
        current_speed = 0

        for i in range(2):
            current_speed += self.velocity[i] * wish_dir[i]

        add_speed = wish_speed - current_speed
        if add_speed <= 0:
            return

        accel_speed = self.accel * delta_time * wish_speed
        if accel_speed > add_speed:
            accel_speed = add_speed

        self.velocity += wish_dir * accel_speed
