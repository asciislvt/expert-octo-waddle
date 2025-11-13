import pykraken as kn
from entity import Entity


class PlayerEntity(Entity):
    def input(self) -> None:
        self.input_direction = kn.Vec2(0, 0)
        self.input_direction.y = kn.key.is_pressed(kn.K_s) - kn.key.is_pressed(kn.K_w)
        self.input_direction.x = kn.key.is_pressed(kn.K_d) - kn.key.is_pressed(kn.K_a)

    def update(self, dt: float) -> None:
        self.handle_velocity(dt)
        self.position += self.velocity * dt

    def draw(self) -> None:
        if self.texture is None:
            kn.draw.rect(
                kn.Rect(self.position.x, self.position.y - 8, 16, 16),
                kn.Color(0, 255, 0),
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
