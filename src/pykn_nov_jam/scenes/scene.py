import pykraken as kn

from pykn_nov_jam.entities.entity_manager import EntityManager
from pykn_nov_jam.globals import Globals
from pykn_nov_jam.follow_camera import FollowCamera
from pykn_nov_jam.scenes.level_data import LevelData
from pykn_nov_jam.spatial_hash import SpatialHash
from pykn_nov_jam.systems.ai_system import AiSystem
from pykn_nov_jam.systems.collision_system import CollisionSystem
from pykn_nov_jam.systems.interaction_system import InteractionSystem


class Scene:
    def __init__(self, level_data: "LevelData") -> None:
        self.entity_manager: EntityManager = EntityManager()
        self.spatial_hash: SpatialHash = SpatialHash()
        self.collision_system: CollisionSystem = CollisionSystem(
            3, self.entity_manager, self.spatial_hash
        )
        self.interaction_system: InteractionSystem = InteractionSystem(
            self.entity_manager, self.spatial_hash
        )
        self.ai_system = AiSystem(self.entity_manager)
        self.visual_layers: dict[int, kn.Texture] = level_data.sprite_layers

        for entity in level_data.entities:
            self.entity_manager.add_entity(entity)
        if Globals._instance is None:
            raise Exception("Globals singleton instance is not initialized.")
        self.main_camera = FollowCamera(
            Globals._instance.get_player_entity(), kn.Vec2(0, 0), 2.0, 0.8
        )
        self.main_camera.set()
        self.scale_shader = kn.ShaderState("assets/shaders/scale.spv", 1)

    def process_scene(self, delta_time: float) -> None:
        kn.renderer.clear(kn.color.BLACK)

        self.ai_system.process_ai(delta_time)
        for entity in self.entity_manager.get_entities():
            for component in entity.component_collection.values():
                component.process_input()
                component.process_update(kn.time.get_delta())

        self.collision_system.process_collisions(delta_time)
        self.interaction_system.process_interactions()

        self.main_camera.update(kn.time.get_delta())
        self.scale_shader.set_uniform(0, self.main_camera.uniform_buffer.to_bytes())

        for layer in self.visual_layers.keys():
            background: kn.Texture = self.visual_layers[layer]
            background_rect = kn.Rect(0, 0, background.size * 2)
            kn.renderer.draw(background, background_rect)

        for entity in self.entity_manager.get_entities():
            for component in entity.component_collection.values():
                component.process_draw()

        self.scale_shader.bind()
        kn.renderer.present()
        self.scale_shader.unbind()

    def get_collision_system(self) -> CollisionSystem:
        return self.collision_system

    def get_entity_manager(self) -> EntityManager:
        return self.entity_manager
