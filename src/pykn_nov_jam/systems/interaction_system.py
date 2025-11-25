import pykraken as kn

from pykn_nov_jam.components.interaction.interactable_component import (
    InteractableComponent,
)

from pykn_nov_jam.entities.entity import Entity
from pykn_nov_jam.entities.entity_manager import EntityManager
from pykn_nov_jam.spatial_hash import SpatialHash
from pykn_nov_jam.globals import Globals


class InteractionSystem:
    def __init__(
        self, entity_manager: EntityManager, spatial_hash: SpatialHash
    ) -> None:
        self.entity_manager: EntityManager = entity_manager
        self.spatial_hash = spatial_hash
        self.player_entity: Entity | None = (
            Globals._instance.get_player_entity() if Globals._instance else None
        )
        self.max_interaction_distance: float = 32.0

    def process_interactions(self):
        entities = self.spatial_hash.get_neighbor_entites_with_component(
            self.player_entity,  # type: ignore
            InteractableComponent,
        )

        if len(entities) == 0:
            return

        nearest_entity = self.get_nearest_entity(self.player_entity, entities)  # type: ignore
        if nearest_entity is None:
            return

        interactalbe_component: InteractableComponent = nearest_entity.get_component(
            InteractableComponent  # type: ignore
        )

        if kn.key.is_just_pressed(kn.K_f):
            if interactalbe_component is not None:
                interactalbe_component.interact()

    def get_nearest_entity(
        self, entity: Entity, neighbors: list[Entity]
    ) -> Entity | None:
        result: Entity | None = None
        current_nearest_distance = float("inf")
        source_position = entity.position
        for neighbor in neighbors:
            source_to_neighbor = neighbor.position - source_position
            if source_to_neighbor.length > self.max_interaction_distance:
                continue
            if source_to_neighbor.length >= current_nearest_distance:
                continue
            if source_to_neighbor.length < current_nearest_distance:
                current_nearest_distance = source_to_neighbor.length
                result = neighbor
        if result is not None:
            kn.draw.line(
                kn.Line(self.player_entity.position, result.position),  # type: ignore
                kn.Color(255, 0, 0),
                3,
            )
        return result
