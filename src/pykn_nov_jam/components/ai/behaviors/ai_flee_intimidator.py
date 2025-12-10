import pykraken as kn

from pykn_nov_jam.components.ai.ai_input_data import AiInputData
from pykn_nov_jam.components.ai.behaviors.ai_behavior import AiBehavior
from pykn_nov_jam.components.intimidation_component import IntimidationComponent
from pykn_nov_jam.entities.entity import Entity


class AiFleeIntimidator(AiBehavior):
    def __init__(
        self, entity: Entity, priority: int, flee_distance: float = 64
    ) -> None:
        super().__init__(entity, priority)
        self.flee_distance_threshold = flee_distance
        self.nearest_intimidator: Entity | None = None

    def evaluate_behavior(self, delta_time: float, input_data: AiInputData) -> float:
        if input_data.spatial_hash is None:
            return 0.0
        intimitators = input_data.spatial_hash.get_neighbor_entites_with_component(
            self.entity, IntimidationComponent
        )
        intimitator = self.get_nearest_entity(self.entity, intimitators)
        if intimitator is not None:
            self.nearest_intimidator = intimitator
            # print(f"Found nearest intimidator at position {intimitator.position}")
            return 1.0  # Need to flee

        return 0.0  # No need to flee

    def get_steering_vector(self, input_data: AiInputData) -> kn.Vec2:
        result: kn.Vec2 = kn.Vec2(0, 0)
        if self.nearest_intimidator is None:
            print("AiFleeIntimidator: No nearest intimidator found!")
            return result
        if self.steering is None:
            print("AiFleeIntimidator: No steering component found!")
            return result
        result = self.steering.seek(self.nearest_intimidator.position, True)
        return result

    def get_nearest_entity(
        self, entity: Entity, neighbors: list[Entity]
    ) -> Entity | None:
        result: Entity | None = None
        current_nearest_distance = float("inf")
        source_position = entity.position
        for neighbor in neighbors:
            source_to_neighbor = neighbor.position - source_position
            if source_to_neighbor.length > self.flee_distance_threshold:
                continue
            if source_to_neighbor.length >= current_nearest_distance:
                continue
            if source_to_neighbor.length < current_nearest_distance:
                current_nearest_distance = source_to_neighbor.length
                result = neighbor

        return result
