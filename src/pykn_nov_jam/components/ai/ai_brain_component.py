import pykraken as kn

from pykn_nov_jam.components.ai.ai_input_data import AiInputData
from pykn_nov_jam.components.ai.ai_steering_component import AiSteeringComponent
from pykn_nov_jam.components.ai.behaviors.ai_behavior import AiBehavior
from pykn_nov_jam.components.component import Component
from pykn_nov_jam.entities.entity import Entity


class AiBrainComponent(Component):
    def __init__(self, entity: Entity) -> None:
        super().__init__(entity)
        self.steering: AiSteeringComponent = entity.get_component(AiSteeringComponent)  # type: ignore
        self.input_data: AiInputData = AiInputData()
        self.behaviors: list[AiBehavior] = []
        # TODO: Implement fear levels

    def add_behavior(self, behavior: AiBehavior) -> None:
        self.behaviors.append(behavior)

    def set_input_data(self, input_data: AiInputData) -> None:
        self.input_data = input_data

    def process_update(self, delta_time: float) -> None:
        if self.enabled is False:
            return

        total_weight = 0.0
        steering_result = kn.Vec2(0, 0)

        print("-----")
        print(f"Processing AI Brain for entity position: {self.entity.position}")
        for behavior in self.behaviors:
            if behavior.enabled is False:
                continue

            # print(f"Processing behavior: {behavior.__class__.__name__}")
            print(f"Behavior: {behavior.__class__.__name__}")
            weight = behavior.evaluate_behavior(delta_time, self.input_data)
            behavior.weight = weight
            print(f"\tBehavior weight: {weight}")

            if weight > 0.0:
                steering_vector = behavior.get_steering_vector(self.input_data)
                print(f"Steering vector from behavior: {steering_vector}")
                steering_result += steering_vector * weight
                total_weight += weight

        print(f"Total steering weight: {total_weight}")
        if total_weight > 0.0:
            steering_result /= total_weight
            steering_result.normalize()
            print(f"Steering result vector: {steering_result}")
            if steering_result.length > 0:
                self.steering.input_direction = steering_result
                print(
                    f"Steering input direction set to: {self.steering.input_direction}"
                )
        print("-----")
