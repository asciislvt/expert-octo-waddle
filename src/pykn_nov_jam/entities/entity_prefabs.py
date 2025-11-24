import pykraken as kn

from typing import Callable
from pykn_nov_jam.components.interaction.interaction_component import (
    InteractionComponent,
)
from pykn_nov_jam.globals import Globals
from pykn_nov_jam.components.ai.ai_brain_component import AiBrainComponent
from pykn_nov_jam.components.ai.ai_steering_component import AiSteeringComponent
from pykn_nov_jam.components.collision_component import CollisionComponent
from pykn_nov_jam.components.key_input_component import InputComponent
from pykn_nov_jam.components.movement_component import MovementComponent
from pykn_nov_jam.components.sprite_component import SpriteComponent
from pykn_nov_jam.components.whistle_component import WhistleComponent
from pykn_nov_jam.entities.entity import Entity


class EntityPrefabs:
    @staticmethod
    def create_entity_from_data(entity_data: dict) -> Entity:
        entity_type = entity_data["id"]
        pos_x = entity_data["x"] * 2
        pos_y = entity_data["y"] * 2
        entity_position = kn.Vec2(pos_x, pos_y)
        custom_fields = entity_data["customFields"]

        print(f"Creating entity of type: {entity_type}")
        if entity_type not in EntityPrefabs.entity_types:
            print(f"Warning: Entity type '{entity_type}' not found in prefabs.")
            return Entity()
        entity = EntityPrefabs.entity_types[entity_type](entity_position, custom_fields)

        return entity

    @staticmethod
    def create_player(position: kn.Vec2, custom_params: dict = {}) -> Entity:
        accel: float = custom_params.get("accel", 80.0)
        decel: float = custom_params.get("decel", 20.0)
        max_speed: float = custom_params.get("max_speed", 40.0)
        player: Entity = Entity(position)

        player.add_component(InputComponent(player))
        player.add_component(InteractionComponent(player))
        player.add_component(SpriteComponent(player, "assets/sprites/player.png"))
        player.add_component(MovementComponent(player, accel, decel, max_speed))
        player.add_component(WhistleComponent(player))
        player.add_component(
            CollisionComponent(
                player,
                kn.Rect(position, 14, 14),
                "dynamic",
                # on_collide=_player_on_collide,
            )
        )
        if Globals._instance is None:
            raise Exception("Globals singleton instance is not initialized.")

        Globals._instance.set_player_entity(player)

        # print("Player entity created at position: %r" % position)
        return player

    @staticmethod
    def create_sheep(position: kn.Vec2, custom_params: dict = {}) -> Entity:
        sheep: Entity = Entity(position)

        sheep.add_component(AiSteeringComponent(sheep))
        sheep.add_component(AiBrainComponent(sheep))
        sheep.add_component(MovementComponent(sheep, 60, 10, 20))
        sheep.add_component(CollisionComponent(sheep, kn.Rect(sheep.position, 14, 14)))
        sheep.add_component(SpriteComponent(sheep, "assets/sprites/sheep.png"))

        # print("Sheep entity created at position: %r" % position)
        return sheep

    @staticmethod
    def create_container(position: kn.Vec2, custom_params: dict = {}) -> Entity:
        container: Entity = Entity(position)

        container.add_component(
            SpriteComponent(container, "assets/sprites/container-chest.png")
        )
        container.add_component(
            CollisionComponent(container, kn.Rect(container.position, 16, 16))
        )

        return container

    @staticmethod
    def create_static_object(
        position: kn.Vec2, width: int = 16, height: int = 16
    ) -> Entity:
        static_object: Entity = Entity(position)

        static_object.add_component(SpriteComponent(static_object, None, width, height))
        static_object.add_component(
            CollisionComponent(
                static_object, kn.Rect(static_object.position, width, height), "static"
            )
        )

        # print("Static object entity created at position: %r" % position)
        return static_object

    @staticmethod
    def create_collision_block(position: kn.Vec2, collision_rect: kn.Rect) -> Entity:
        pos: kn.Vec2 = kn.Vec2(collision_rect.x, collision_rect.y)
        collision_block: Entity = Entity(pos)

        collision_block.add_component(
            CollisionComponent(
                collision_block,
                collision_rect,
                "static",
            )
        )

        # print("Collision block entity created at position: %r" % position)
        return collision_block

    # NOTE: Add new entity types here, lol
    entity_types: dict[str, Callable] = {
        "Player": create_player,
        "Sheep": create_sheep,
        "Container": create_container,
    }


# def _player_on_collide(player: Entity, other_entity: Entity) -> None:
#     if other_entity.has_component(CollisionComponent):
#         other_collision: CollisionComponent = other_entity.get_component(
#             CollisionComponent
#         )  # type: ignore
#         if other_collision.body_type == "static":
#             movement: MovementComponent = player.get_component(MovementComponent)  # type: ignore
