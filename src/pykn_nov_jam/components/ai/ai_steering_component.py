import pykraken as kn
from entities.entity import Entity
from components.key_input_component import InputComponent
from components.movement_component import MovementComponent


class AiSteeringComponent(InputComponent):
    def __init__(
        self,
        entity: Entity,
        target_entity: Entity | None = None,
    ) -> None:
        super().__init__(entity)
        self.target_entity: Entity | None = target_entity

    def process_input(self) -> None:
        steering = self.calculate_steering()
        self.input_direction = steering

    def calculate_steering(self) -> kn.Vec2:
        if self.target_entity is None:
            print("AiSteeringComponent: No target entity set for steering!")
            return kn.Vec2(0, 0)
        else:
            velocity_component = self.entity.get_component(MovementComponent)  # type: ignore
            dir_to_target = kn.Vec2(0, 0)
            dir_to_target = self.target_entity.position - self.entity.position
            dir_to_target.normalize()

            wish_velocity = dir_to_target * velocity_component.max_speed
            steer_velocity = wish_velocity - velocity_component.velocity

            steer_velocity.normalize()
            return steer_velocity
