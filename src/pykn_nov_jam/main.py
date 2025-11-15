import follow_camera as fc
import pykraken as kn
from entities.entity_prefabs import EntityPrefabs
from globals import Globals


kn.init()
kn.window.create("The Herdsman", kn.Vec2(480, 432))
kn.time.set_target(30)

entities = []
global_singleton = Globals()

player = EntityPrefabs.create_player(kn.Vec2(240, 216), global_singleton)
entities.append(player)

for i in range(5):
    sheep = EntityPrefabs.create_sheep(
        kn.Vec2(50 * i + 50, 50), global_singleton.get_player_entity()
    )
    entities.append(sheep)

main_camera = fc.FollowCamera(
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

    for entity in entities:
        for component in entity.component_collection.values():
            component.process_input()
            component.process_update(kn.time.get_delta())
            component.process_draw()

    main_camera.update(kn.time.get_delta())
    scale_shader.set_uniform(0, main_camera.uniform_buffer.to_bytes())

    scale_shader.bind()
    kn.renderer.present()
    scale_shader.unbind()

kn.quit()
