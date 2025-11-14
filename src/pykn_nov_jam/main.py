import pykraken as kn
import follow_camera as fc

from globals import Globals
from entities.entity import Entity
from components.key_input_component import InputComponent
from components.movement_component import MovementComponent
from components.sprite_component import SpriteComponent
from components.ai.ai_steering_component import AiSteeringComponent


kn.init()
kn.window.create("Kraken Example", kn.Vec2(480, 432))

global_singleton = Globals()

entities = []

player: Entity = Entity(kn.Vec2(240, 216))

player.add_component(InputComponent(player))
player.add_component(SpriteComponent(player, "assets/player.png"))
player.add_component(MovementComponent(player, 160, 12, 100))
global_singleton.set_player_entity(player)
entities.append(player)

for i in range(5):
    ent = Entity(kn.Vec2(50 * i + 100, 50 * i + 100))
    ent.add_component(AiSteeringComponent(ent, player))
    ent.add_component(SpriteComponent(ent, "assets/sheep.png"))
    ent.add_component(MovementComponent(ent, 58, 10, 15))
    entities.append(ent)


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
