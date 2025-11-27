import pykraken as kn

from pykn_nov_jam.components.ai.ai_brain_component import AiBrainComponent
from pykn_nov_jam.components.ai.ai_input_data import AiInputData
from pykn_nov_jam.components.ai.behaviors.ai_behavior import AiBehavior
from pykn_nov_jam.components.grazeable_component import GrazeableComponent
from pykn_nov_jam.components.satiety_component import SatietyComponent


class AiGrazingBehavior(AiBehavior):
    def __init__(self, entity, priority: int, is_exclusive: bool = True) -> None:
        super().__init__(entity, priority, is_exclusive)
        self.brain_component: AiBrainComponent = entity.get_component(AiBrainComponent)  # type: ignore
        self.satiety_component: SatietyComponent = entity.get_component(
            SatietyComponent
        )  # type: ignore

    def evaluate_behavior(self, delta_time: float, input_data: AiInputData) -> float:
        if self.brain_component is None:
            print("\tNo brain component found for grazing behavior.")
            return 0.0

        target_grazeable = self.brain_component.target_grazeable

        if target_grazeable is None:
            return 0.0

        grazeable_component: GrazeableComponent = target_grazeable.get_component(
            GrazeableComponent
        )  # type: ignore
        distance_to_grazeable = self.entity.position.distance_to(
            target_grazeable.position
        )

        if distance_to_grazeable <= grazeable_component.min_eating_radius:
            print(
                f"\tEntity is within minimum eating radius of grazeable {target_grazeable}. Grazing behavior activated."
            )
            if self.satiety_component.satiety == self.satiety_component.max_satiety:
                print("Entity is full!")
                return 0.0

            if self.satiety_component:
                self.satiety_component.recover_satiety(delta_time)
            if grazeable_component:
                grazeable_component.deplete_nutrition(
                    grazeable_component.nutrition_value * delta_time
                )
            print("\tEntity is grazing! recovering satiety.")
            return 1.0
        # elif distance_to_grazeable <= grazeable_component.max_eating_radius:
        #     print(
        #         f"\tEntity is within eating radius of grazeable {target_grazeable}. Grazing behavior activated."
        #     )
        #     return 0.8

        return 0.0

    def get_steering_vector(self, input_data: AiInputData) -> kn.Vec2:
        return kn.Vec2(0, 0)
