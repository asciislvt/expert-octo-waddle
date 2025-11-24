from pykn_nov_jam.components.interaction.interactable_component import (
    InteractableComponent,
)
from pykn_nov_jam.entities.entity_manager import EntityManager
from pykn_nov_jam.spatial_hash import SpatialHash


class InteractionSystem:
    def __init__(
        self, entity_manager: EntityManager, spatial_hash: SpatialHash
    ) -> None:
        self.entity_manager: EntityManager = entity_manager
        self.spatial_hash = spatial_hash

    def process_interactions(self):
        entities = self.entity_manager.get_entities_with_component(
            InteractableComponent
        )
