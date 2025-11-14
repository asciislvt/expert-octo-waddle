import pykraken as kn
import follow_camera as fc

from globals import Globals
from components.key_input_component import KeyInputComponent
from components.movement_component import MovementComponent
from components.sprite_component import SpriteComponent
from entities.entity import Entity


kn.init()
kn.window.create("Kraken Example", kn.Vec2(480, 432))

global_singleton = Globals()

player = Entity(kn.Vec2(240, 216))
player.add_component(KeyInputComponent(player))
player.add_component(SpriteComponent(player, "assets/player.png"))
player.add_component(MovementComponent(player, 200, 50, 100))

global_singleton.set_player_entity(player)

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

    for component in player.component_collection.values():
        component.process_input()
        component.process_update(kn.time.get_delta())
        component.process_draw()

    main_camera.update(kn.time.get_delta())
    scale_shader.set_uniform(0, main_camera.uniform_buffer.to_bytes())

    scale_shader.bind()
    kn.renderer.present()
    scale_shader.unbind()

kn.quit()
