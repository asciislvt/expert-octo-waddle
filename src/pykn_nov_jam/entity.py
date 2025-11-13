import pykraken as kn


class Entity:
    def __init__(
        self,
        position: kn.Vec2,
        texture: kn.Texture | None = None,
        accel: float = 150.0,
        decel: float = 100.0,
        max_speed: float = 20.0,
    ) -> None:
        self.texture: kn.Texture | None = texture if texture is not None else None
        self.position: kn.Vec2 = position
        self.velocity: kn.Vec2 = kn.Vec2(0, 0)
        self.input_direction: kn.Vec2 = kn.Vec2(0, 0)
        self.max_speed: float = max_speed
        self.accel: float = accel
        self.decel: float = decel

    def update(self, dt: float) -> None:
        pass

    def input(self) -> None:
        pass

    def draw(self) -> None:
        pass
