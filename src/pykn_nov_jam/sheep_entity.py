import pykraken as kn
from entity import Entity
import globals


class SheepEntity(Entity):
    def __init__(
        self,
        position: kn.Vec2,
        texture: kn.Texture | None = None,
    ) -> None:
        super().__init__(position, texture)
        if globals.Globals._instance is None:
            print("Globals instance is not initialized, cannot get player entity.")
            self.player_entity = None
        else:
            self.player_entity = globals.Globals._instance.get_player_entity()

    def input(self) -> None:
        self.input_direction = self.seek(True)

    def update(self, dt: float) -> None:
        self.handle_velocity(dt)
        self.position += self.velocity * dt

    def draw(self) -> None:
        if self.texture is None:
            kn.draw.rect(
                kn.Rect(self.position.x, self.position.y - 8, 16, 16),
                kn.Color(0, 150, 255),
            )
        else:
            kn.renderer.draw(self.texture, kn.Rect(self.position, 16, 16))

    def handle_velocity(self, delta_time: float):
        self.velocity -= self.velocity * self.decel * delta_time

        wish_speed = self.input_direction.length * self.max_speed
        self.accelerate(self.input_direction, wish_speed, delta_time)

    def accelerate(self, wish_dir: kn.Vec2, wish_speed: float, delta_time: float):
        current_speed = 0

        for i in range(2):
            current_speed += self.velocity[i] * wish_dir[i]

        add_speed = wish_speed - current_speed
        if add_speed <= 0:
            return

        accel_speed = self.accel * delta_time * wish_speed
        if accel_speed > add_speed:
            accel_speed = add_speed

        self.velocity += wish_dir * accel_speed

    def seek(self, flee: bool = False) -> kn.Vec2:
        debug_wish_steer = kn.Line(
            self.position, self.position + self.input_direction * 16
        )
        kn.draw.line(debug_wish_steer, kn.Color(255, 0, 0))
        if self.player_entity is not None:
            dir_to_player = kn.Vec2(0, 0)
            if flee:
                dir_to_player = self.position - self.player_entity.position
            else:
                dir_to_player = self.player_entity.position - self.position

            dir_to_player.normalize()
            wish_velocity = dir_to_player * self.max_speed
            steering = wish_velocity - self.velocity

            if steering.length > 0:
                steering.normalize()
                return steering

        print("Player entity is None, cannot compute steering.")
        return kn.Vec2(0, 0)
