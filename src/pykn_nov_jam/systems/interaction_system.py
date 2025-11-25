import pykraken as kn

from pykn_nov_jam.components.interaction.interactable_component import (
    InteractableComponent,
)

from pykn_nov_jam.components.label_component import LabelComponent
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
        self.current_interactable: Entity | None = None

    def process_interactions(self):
        entities = self.spatial_hash.get_neighbor_entites_with_component(
            self.player_entity,  # type: ignore
            InteractableComponent,
        )

        if len(entities) == 0:
            return

        nearest_entity = self.get_nearest_entity(self.player_entity, entities)  # type: ignore
        if nearest_entity is None:
            if self.current_interactable is not None:
                self.current_interactable.get_component(LabelComponent).visible = False  # type: ignore
                self.current_interactable = None
            return
        if nearest_entity != self.current_interactable:
            self.current_interactable = nearest_entity

        interactable_component: InteractableComponent = nearest_entity.get_component(
            InteractableComponent  # type: ignore
        )
        label_component: LabelComponent = nearest_entity.get_component(LabelComponent)  # type: ignore
        if label_component is not None:
            label_component.visible = True

        for entity in entities:
            label_comp: LabelComponent = entity.get_component(LabelComponent)  # type: ignore
            if label_comp is not None and entity != nearest_entity:
                label_comp.visible = False

        if kn.key.is_just_pressed(kn.K_f):
            if interactable_component is not None:
                interactable_component.interact()

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
