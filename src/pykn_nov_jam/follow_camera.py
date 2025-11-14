import pykraken as kn
from entities.entity import Entity


class FollowCamera(kn.Camera):
    def __init__(
        self,
        target_entity: Entity | None = None,
        target_position: kn.Vec2 = kn.Vec2(0, 0),
        zoom: float = 1.0,
        smoothness: float = 0.1,
    ):
        super().__init__(target_position)
        self.target_entity = target_entity
        self.smoothness = smoothness
        self.uniform_buffer = FollowCameraUniformBuffer(zoom=zoom)

    def update(self, delta_time: float):
        self.uniform_buffer.update()

        if self.target_entity:
            if self.smoothness > 0.0:
                desired_pos = self.target_entity.position - kn.window.get_size() / 2
                self.pos = kn.math.lerp(
                    self.pos, desired_pos, self.smoothness * delta_time
                )
            else:
                self.pos = self.target_entity.position - kn.window.get_size() / 2
        else:
            self.pos = kn.Vec2(0, 0)
            print("FollowCamera: No target entity to follow!")


class FollowCameraUniformBuffer(kn.ShaderUniform):
    zoom: float

    def update(self):
        if kn.key.is_just_pressed(kn.K_m):
            self.zoom += 0.5
        if kn.key.is_just_pressed(kn.K_n):
            if self.zoom <= 1.0:
                self.zoom = 1.0
            else:
                self.zoom -= 0.5
