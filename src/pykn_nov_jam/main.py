import pykraken as kn
from player_entity import PlayerEntity
from sheep_entity import SheepEntity
from entity_manager import EntityManager
import follow_camera as fc
from globals import Globals


kn.init()
kn.window.create("Kraken Example", kn.Vec2(480, 432))

global_singleton = Globals()
player_texture = kn.Texture("assets/player.png")
sheep_texture = kn.Texture("assets/sheep.png")

entity_manager = EntityManager()
entity_manager.add_entity(PlayerEntity(kn.Vec2(240, 216), player_texture, 200, 50, 100))
global_singleton.set_player_entity(entity_manager.entities[0])

for i in range(5):
    entity_manager.add_entity(SheepEntity(kn.Vec2(100 + i * 32, 100), sheep_texture))


main_camera = fc.FollowCamera(
    global_singleton.get_player_entity(), kn.Vec2(0, 0), 2.0, 0.8
)
main_camera.set()
scale_shader = kn.ShaderState("assets/shaders/scale.spv", 1)

while kn.window.is_open():
    kn.event.poll()

    kn.renderer.clear(kn.color.DARK_GREY)
    kn.draw.rect(kn.Rect(0, 0, 64, 64), kn.Color(50, 50, 50))
    kn.draw.rect(kn.Rect(0, 0, 100, 100), kn.color.RED)
    kn.draw.rect(kn.Rect(100, 200, 100, 100), kn.color.BLUE)

    entity_manager.input()
    entity_manager.update(kn.time.get_delta())
    entity_manager.draw()

    main_camera.update(kn.time.get_delta())
    scale_shader.set_uniform(0, main_camera.uniform_buffer.to_bytes())

    scale_shader.bind()
    kn.renderer.present()
    scale_shader.unbind()

kn.quit()
