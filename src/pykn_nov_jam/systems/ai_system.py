import pykraken as kn
from pykn_nov_jam.components.ai.ai_brain_component import AiBrainComponent
from pykn_nov_jam.components.ai.ai_input_data import AiInputData
from pykn_nov_jam.components.whistle_component import WhistleComponent
from pykn_nov_jam.entities.entity_manager import EntityManager
from pykn_nov_jam.spatial_hash import SpatialHash
from pykn_nov_jam.globals import Globals


class AiSystem:
    def __init__(
        self, entity_manager: "EntityManager", spatial_hash: SpatialHash
    ) -> None:
        self.fear_level: float = 0.0
        self.entity_manager = entity_manager
        self.spatial_hash = spatial_hash

    def get_fear_level(self) -> float:
        return self.fear_level

    def process_ai(self, delta_time: float) -> None:
        entity_list = self.entity_manager.get_entities_with_component(AiBrainComponent)
        print(f"Processing AI for {len(entity_list)} entities.")
        player = Globals._instance.get_player_entity() if Globals._instance else None
        player_whistle: WhistleComponent = (
            player.get_component(WhistleComponent) if player else None
        )  # type: ignore
        input_data = AiInputData()
        input_data.whistle = player_whistle.is_whistling if player_whistle else False
        input_data.player_position = player.position if player else kn.Vec2(0, 0)
        input_data.delta_time = delta_time
        input_data.spatial_hash = self.spatial_hash

        for entity in entity_list:
            entity_brain: AiBrainComponent = entity.get_component(AiBrainComponent)  # type: ignore
            entity_brain.set_input_data(input_data)
            entity_brain.process_update(delta_time)
