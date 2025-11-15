from pykraken import Vec2
from entities.entity import Entity
from components.component import Component
from components.key_input_component import InputComponent


class MovementComponent(Component):
    def __init__(
        self, entity: Entity, accel: float, decel: float, max_speed: float
    ) -> None:
        super().__init__(entity)
        self.entity: Entity = entity
        self.velocity: Vec2 = Vec2(0, 0)
        self.accel: float = accel
        self.decel: float = decel
        self.max_speed: float = max_speed
        # self.input: InputComponent = entity.get_component(InputComponent)  # type: ignore

    def process_update(self, delta_time: float) -> None:
        if self.enabled is False:
            return

        self.velocity -= self.velocity * self.decel * delta_time

        input_component: InputComponent | None = self.entity.get_component(
            InputComponent
        )  # type: ignore

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
