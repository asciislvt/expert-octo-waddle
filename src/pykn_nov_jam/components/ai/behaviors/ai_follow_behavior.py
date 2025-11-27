import pykraken as kn

from pykn_nov_jam.components.ai.ai_input_data import AiInputData
from pykn_nov_jam.components.ai.behaviors.ai_behavior import AiBehavior
from pykn_nov_jam.entities.entity import Entity


class AiFollowBehavior(AiBehavior):
    def __init__(self, entity: Entity, priority: int) -> None:
        super().__init__(entity, priority)
        self.wander_radius: float = 50.0
        self.follow_distance: float = 60.0
        self.max_whistle_distance: float = 128.0
        self.follow_falloff: float = 0.8

    def evaluate_behavior(self, delta_time: float, input_data: AiInputData) -> float:
        distance_to_player = (input_data.player_position - self.entity.position).length
        print(f"\tDistance to Player: {distance_to_player}")
        if input_data.whistle and input_data.fear_level < 0.7:
            if distance_to_player < self.max_whistle_distance:
                print("\tWhistle detected within range.")
                return 1.0
        else:
            if (
                distance_to_player < self.follow_distance
                and input_data.fear_level < 0.5
            ):
                return (
                    1.2
                    - (distance_to_player / self.follow_distance) * self.follow_falloff
                )

        return 0.0

    def get_steering_vector(self, input_data: AiInputData) -> kn.Vec2:
        return (
            self.steering.seek(input_data.player_position)
            if self.steering
            else kn.Vec2(0, 0)
        )
