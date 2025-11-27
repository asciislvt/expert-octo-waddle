import pykraken as kn

from pykn_nov_jam.components.ai.ai_brain_component import AiBrainComponent
from pykn_nov_jam.components.ai.ai_input_data import AiInputData
from pykn_nov_jam.components.ai.behaviors.ai_behavior import AiBehavior
from pykn_nov_jam.components.grazeable_component import GrazeableComponent
from pykn_nov_jam.components.satiety_component import SatietyComponent
from pykn_nov_jam.entities.entity import Entity


class AiSeekFoodBehavior(AiBehavior):
    def __init__(self, entity: Entity, priority: int, seek_radius: float = 128) -> None:
        super().__init__(entity, priority)
        self.satiety_component: SatietyComponent = entity.get_component(
            SatietyComponent
        )  # type: ignore
        self.brain_component: AiBrainComponent = entity.get_component(AiBrainComponent)  # type: ignore
        self.seek_radius = seek_radius
        self.target_entity: Entity | None = None

    def evaluate_behavior(self, delta_time: float, input_data: AiInputData) -> float:
        if self.satiety_component is None:
            print("AiSeekFoodBehavior: SatietyComponent not found.")
            return 0.0

        if self.satiety_component.is_hungry() and input_data.fear_level < 0.5:
            print("\tEntity is hungry, evaluating food seeking behavior.")
            if input_data.spatial_hash is None:
                print("AiSeekFoodBehavior: SpatialHash not provided in AiInputData.")
                return 0.0

            grazeable_entities = input_data.spatial_hash.get_neighbors_within_radius(
                self.entity, self.seek_radius, GrazeableComponent
            )

            if grazeable_entities:
                print(
                    f"\tFound {len(grazeable_entities)} grazeable entities within seek radius."
                )
                return 0.8
            else:
                print("\tNo grazeable entities found within seek radius.")

        self.target_entity = None
        if self.brain_component is None:
            self.brain_component.target_grazeable = None
        return 0.0

    def get_steering_vector(self, input_data: AiInputData) -> kn.Vec2:
        if input_data.spatial_hash is None:
            print("AiSeekFoodBehavior: SpatialHash not provided in AiInputData.")
            return kn.Vec2(0, 0)

        if self.target_entity is None:
            grazeable_entities = input_data.spatial_hash.get_neighbors_within_radius(
                self.entity, self.seek_radius, GrazeableComponent
            )

            target_entity: Entity | None = None
            nearest_distance: float = float("inf")
            for entity in grazeable_entities:
                if target_entity is None:
                    target_entity = entity
                    continue

                distance = entity.position.distance_to(self.entity.position)
                if distance < nearest_distance:
                    nearest_distance = distance
                    target_entity = entity

            self.target_entity = target_entity
            if self.brain_component is None:
                print("AiSeekFoodBehavior: Brain component not found.")
            else:
                self.brain_component.target_grazeable = target_entity

        if self.target_entity:
            if self.steering is None:
                print("AiSeekFoodBehavior: Steering component not found.")
                return kn.Vec2(0, 0)

            return self.steering.seek(self.target_entity.position)

        return kn.Vec2(0, 0)
