from typing import Callable

import pykraken as kn

from pykn_nov_jam.components.ai.ai_brain_component import AiBrainComponent
from pykn_nov_jam.components.ai.ai_steering_component import AiSteeringComponent
from pykn_nov_jam.components.ai.behaviors.ai_follow_behavior import AiFollowBehavior
from pykn_nov_jam.components.ai.behaviors.ai_grazing_behavior import AiGrazingBehavior
from pykn_nov_jam.components.ai.behaviors.ai_seek_food_behavior import (
    AiSeekFoodBehavior,
)
from pykn_nov_jam.components.ai.behaviors.ai_wander_behavior import AiWanderBehavior
from pykn_nov_jam.components.collision_component import CollisionComponent
from pykn_nov_jam.components.grazeable_component import GrazeableComponent
from pykn_nov_jam.components.interaction.interactable_component import (
    InteractableComponent,
)
from pykn_nov_jam.components.interaction.interaction_component import (
    InteractionComponent,
)
from pykn_nov_jam.components.intimidation_component import IntimidationComponent
from pykn_nov_jam.components.key_input_component import KeyInputComponent
from pykn_nov_jam.components.label_component import LabelComponent
from pykn_nov_jam.components.movement_component import MovementComponent
from pykn_nov_jam.components.satiety_component import SatietyComponent
from pykn_nov_jam.components.sprite_component import SpriteComponent
from pykn_nov_jam.components.whistle_component import WhistleComponent
from pykn_nov_jam.entities.entity import Entity
from pykn_nov_jam.globals import Globals


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

        player.add_component(KeyInputComponent(player))
        player.add_component(InteractionComponent(player))
        player.add_component(SpriteComponent(player, "assets/sprites/player.png"))
        player.add_component(MovementComponent(player, accel, decel, max_speed))
        player.add_component(WhistleComponent(player))
        player.add_component(
            CollisionComponent(
                player,
                kn.Rect(position, 14, 14),
                "dynamic",
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
        sheep.add_component(MovementComponent(sheep, 60, 10, 20))
        sheep.add_component(CollisionComponent(sheep, kn.Rect(sheep.position, 14, 14)))
        sheep.add_component(SpriteComponent(sheep, "assets/sprites/sheep.png"))
        sheep.add_component(SatietyComponent(sheep, 100.0))

        brain: AiBrainComponent = AiBrainComponent(sheep)
        sheep.add_component(brain)
        brain.add_behavior(AiFollowBehavior(sheep, 2))
        brain.add_behavior(AiWanderBehavior(sheep, 1))
        brain.add_behavior(AiSeekFoodBehavior(sheep, 3))
        brain.add_behavior(AiGrazingBehavior(sheep, 4))

        # print("Sheep entity created at position: %r" % position)
        return sheep

    @staticmethod
    def create_chupacabra(position: kn.Vec2, custom_params: dict = {}) -> Entity:
        chupacabra: Entity = Entity(position)

        chupacabra.add_component(AiSteeringComponent(chupacabra))
        chupacabra.add_component(MovementComponent(chupacabra, 80, 15, 30))
        chupacabra.add_component(
            CollisionComponent(chupacabra, kn.Rect(chupacabra.position, 16, 16))
        )
        chupacabra.add_component(
            SpriteComponent(chupacabra, "assets/sprites/chupacabra.png")
        )
        chupacabra.add_component(IntimidationComponent(chupacabra))
        # chupacabra.add_component(SatietyComponent(chupacabra, 150.0))

        brain: AiBrainComponent = AiBrainComponent(chupacabra)
        chupacabra.add_component(brain)
        # brain.add_behavior(AiFollowBehavior(chupacabra, 2))
        brain.add_behavior(AiWanderBehavior(chupacabra, 1))
        # brain.add_behavior(AiSeekFoodBehavior(chupacabra, 3))

        # print("Chupacabra entity created at position: %r" % position)
        return chupacabra

    @staticmethod
    def create_grazing_field(position: kn.Vec2, custom_params: dict = {}) -> Entity:
        grazing_field: Entity = Entity(position)

        grazing_field.add_component(GrazeableComponent(grazing_field, 64))
        grazing_field.add_component(
            CollisionComponent(
                grazing_field, kn.Rect(grazing_field.position, 1, 1), "area"
            )
        )
        grazing_field.add_component(
            SpriteComponent(grazing_field, "assets/sprites/container-chest.png", 32, 32)
        )
        return grazing_field

    @staticmethod
    def create_container(position: kn.Vec2, custom_params: dict = {}) -> Entity:
        container: Entity = Entity(position)

        def on_interact(entity: Entity) -> None:
            print("Interacted with container at position: %r" % entity.position)

        container.add_component(
            SpriteComponent(container, "assets/sprites/container-chest.png")
        )
        container.add_component(
            CollisionComponent(container, kn.Rect(container.position, 16, 16))
        )
        container.add_component(InteractableComponent(container, on_interact))
        container.add_component(
            LabelComponent(
                container, "Container\n (F) - Use", kn.color.WHITE, kn.Vec2(14, -24)
            )
        )

        return container

    @staticmethod
    def create_door(position: kn.Vec2, custom_params: dict = {}) -> Entity:
        door: Entity = Entity(position)

        def on_interact(entity: Entity) -> None:
            print("Interacted with door at position: %r" % entity.position)
            collision: CollisionComponent = entity.get_component(CollisionComponent)  # type: ignore
            sprite: SpriteComponent = entity.get_component(SpriteComponent)  # type: ignore
            if collision:
                collision.enabled = not collision.enabled
                print(f"Collision enabled: {collision.enabled}")
            if sprite:
                if collision.enabled:
                    sprite.offset_source_rect(0, 0)
                else:
                    sprite.offset_source_rect(8, 0)

        # TODO: Add door sprites and animation
        # door.add_component(
        #     SpriteComponent(door, "assets/sprites/door-closed.png", 16, 16)
        # )
        door.add_component(
            SpriteComponent(
                door, "assets/sprites/door.png", 16, 16, 0, 0, kn.Rect(0, 0, 8, 8)
            )
        )
        door.add_component(
            CollisionComponent(door, kn.Rect(door.position, 16, 16), "static")
        )
        door.add_component(InteractableComponent(door, on_interact))
        door.add_component(
            LabelComponent(door, "Door\n (F) - Use", kn.color.WHITE, kn.Vec2(22, -16))
        )

        return door

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
        "Chupacabra": create_chupacabra,
        "Container": create_container,
        "Door": create_door,
        "GrazingField": create_grazing_field,
    }
