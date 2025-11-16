import pykraken as kn

from pykn_nov_jam.entities.entity_manager import EntityManager
from pykn_nov_jam.entities.entity_prefabs import EntityPrefabs
from pykn_nov_jam.follow_camera import FollowCamera
from pykn_nov_jam.globals import Globals
from pykn_nov_jam.spatial_hash import SpatialHash
from pykn_nov_jam.systems.collision_system import CollisionSystem

kn.init()
kn.window.create("The Herdsman", kn.Vec2(480, 432))
kn.time.set_target(60)

entities = EntityManager()
global_singleton = Globals()
hash_map = SpatialHash()
collision_system = CollisionSystem()

player = EntityPrefabs.create_player(kn.Vec2(240, 216), global_singleton)
entities.add_entity(player)

static_object = EntityPrefabs.create_static_object(kn.Vec2(128, 198), 128, 16)
entities.add_entity(static_object)

for i in range(5):
    sheep = EntityPrefabs.create_sheep(
        kn.Vec2(50 * i + 50, 50), global_singleton.get_player_entity()
    )
    entities.add_entity(sheep)

main_camera = FollowCamera(
    global_singleton.get_player_entity(), kn.Vec2(0, 0), 2.0, 0.8
)
main_camera.set()
scale_shader = kn.ShaderState("assets/shaders/scale.spv", 1)


while kn.window.is_open():
    kn.event.poll()

    kn.renderer.clear(kn.color.BLACK)
    kn.draw.rect(kn.Rect(0, 0, 64, 64), kn.Color(50, 50, 50))
    kn.draw.rect(kn.Rect(0, 0, 100, 100), kn.color.RED)
    kn.draw.rect(kn.Rect(100, 200, 100, 100), kn.color.BLUE)

    for entity in entities.get_entities():
        for component in entity.component_collection.values():
            component.process_input()
            component.process_update(kn.time.get_delta())

    collision_system.process_components(kn.time.get_delta())

    for entity in entities.get_entities():
        for component in entity.component_collection.values():
            component.process_draw()

    main_camera.update(kn.time.get_delta())
    scale_shader.set_uniform(0, main_camera.uniform_buffer.to_bytes())
    hash_map.debug_draw_cells()

    scale_shader.bind()
    kn.renderer.present()
    scale_shader.unbind()

kn.quit()
