import globals
import pykraken as kn
from components.ai.ai_steering_component import AiSteeringComponent
from components.key_input_component import InputComponent
from components.movement_component import MovementComponent
from components.sprite_component import SpriteComponent
from components.collision_component import CollisionComponent
from entities.entity import Entity


class EntityPrefabs:
    @staticmethod
    def create_player(position: kn.Vec2, global_singleton: globals.Globals) -> Entity:
        player: Entity = Entity(position)

        player.add_component(InputComponent(player))
        player.add_component(SpriteComponent(player, "assets/sprites/player.png"))
        player.add_component(MovementComponent(player, 160, 12, 100))
        player.add_component(
            CollisionComponent(player, kn.Rect(player.position, 16, 16))
        )
        global_singleton.set_player_entity(player)

        print("Player entity created at position: %r" % position)
        return player

    @staticmethod
    def create_sheep(position: kn.Vec2, target_entity: Entity | None) -> Entity:
        sheep: Entity = Entity(position)

        sheep.add_component(AiSteeringComponent(sheep, target_entity))
        sheep.add_component(SpriteComponent(sheep, "assets/sprites/sheep.png"))
        sheep.add_component(MovementComponent(sheep, 70, 10, 30))

        print("Sheep entity created at position: %r" % position)
        return sheep

    @staticmethod
    def create_static_object(position: kn.Vec2) -> Entity:
        static_object: Entity = Entity(position)

        static_object.add_component(SpriteComponent(static_object, "", 16, 16))
        static_object.add_component(
            CollisionComponent(static_object, kn.Rect(static_object.position, 16, 16))
        )

        print("Static object entity created at position: %r" % position)
        return static_object
