from pykraken import Vec2
from entities.entity import Entity
from components.component import Component
from components.key_input_component import KeyInputComponent


class MovementComponent(Component):
    def __init__(self, entity: Entity, accel: float, decel: float, max_speed: float):
        self.entity: Entity = entity
        self.accel: float = accel
        self.decel: float = decel
        self.max_speed: float = max_speed
        self.input: KeyInputComponent = entity.get_component(KeyInputComponent)  # type: ignore

    def process_update(self, delta_time: float):
        self.entity.velocity -= self.entity.velocity * self.decel * delta_time

        wish_speed = self.input.input_direction.length * self.max_speed
        self.accelerate(self.input.input_direction, wish_speed, delta_time)

        self.entity.position += self.entity.velocity * delta_time

    def accelerate(self, wish_dir: Vec2, wish_speed: float, delta_time: float):
        current_speed = 0

        for i in range(2):
            current_speed += self.entity.velocity[i] * wish_dir[i]

        add_speed = wish_speed - current_speed
        if add_speed <= 0:
            return

        accel_speed = self.accel * delta_time * wish_speed
        if accel_speed > add_speed:
            accel_speed = add_speed

        self.entity.velocity += wish_dir * accel_speed
