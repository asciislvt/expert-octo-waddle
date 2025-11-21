import pykraken as kn

from pykn_nov_jam.scenes.scene_manager import SceneManager
from pykn_nov_jam.globals import Globals

kn.init()
kn.window.create("The Herdsman", kn.Vec2(480, 432))
kn.time.set_target(60)

global_singleton = Globals()
scene_manager = SceneManager("raw/ldtk/test_map")
scene_manager.current_scene = scene_manager.load_scene("Scene_0")

while kn.window.is_open():
    kn.event.poll()
    scene_manager.current_scene.process_scene(kn.time.get_delta())

kn.quit()
