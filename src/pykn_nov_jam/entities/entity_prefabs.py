import pykraken as kn

from pykn_nov_jam import globals
from pykn_nov_jam.components.ai.ai_steering_component import AiSteeringComponent
from pykn_nov_jam.components.collision_component import CollisionComponent
from pykn_nov_jam.components.key_input_component import InputComponent
from pykn_nov_jam.components.movement_component import MovementComponent
from pykn_nov_jam.components.sprite_component import SpriteComponent
from pykn_nov_jam.entities.entity import Entity


def _player_on_collide(player: Entity, other_entity: Entity) -> None:
    if other_entity.has_component(CollisionComponent):
        other_collision: CollisionComponent = other_entity.get_component(
            CollisionComponent
        )  # type: ignore
        if other_collision.body_type == "static":
            movement: MovementComponent = player.get_component(MovementComponent)  # type: ignore


class EntityPrefabs:
    @staticmethod
    def create_player(position: kn.Vec2, global_singleton: globals.Globals) -> Entity:
        player: Entity = Entity(position)

        player.add_component(InputComponent(player))
        player.add_component(SpriteComponent(player, "assets/sprites/player.png"))
        player.add_component(MovementComponent(player, 160, 12, 100))
        player.add_component(
            CollisionComponent(
                player,
                kn.Rect(player.position, 16, 16),
                "dynamic",
                on_collide=_player_on_collide,
            )
        )
        global_singleton.set_player_entity(player)

        print("Player entity created at position: %r" % position)
        return player

    @staticmethod
    def create_sheep(
        position: kn.Vec2, target_entity: Entity | None, fleeing: bool = False
    ) -> Entity:
        sheep: Entity = Entity(position)

        sheep.add_component(AiSteeringComponent(sheep, target_entity, fleeing))
        sheep.add_component(SpriteComponent(sheep, "assets/sprites/sheep.png"))
        sheep.add_component(MovementComponent(sheep, 70, 10, 30))
        sheep.add_component(CollisionComponent(sheep, kn.Rect(sheep.position, 16, 16)))

        print("Sheep entity created at position: %r" % position)
        return sheep

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

        print("Static object entity created at position: %r" % position)
        return static_object
