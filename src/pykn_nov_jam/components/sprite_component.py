import pykraken as kn
from components.component import Component
from entities.entity import Entity


class SpriteComponent(Component):
    def __init__(self, entity: Entity, sprite_path: str):
        super().__init__(entity)
        self.sprite_path: str = sprite_path
        self.sprite: kn.Texture | None = None
        self.load_sprite()

    def load_sprite(self) -> None:
        self.sprite = kn.Texture(self.sprite_path)

    def process_draw(self) -> None:
        if self.sprite is None:
            kn.draw.rect(
                kn.Rect(self.entity.position.x, self.entity.position.y - 8, 16, 16),
                kn.Color(0, 255, 0),
            )
        else:
            kn.renderer.draw(
                self.sprite,
                kn.Rect(self.entity.position.x, self.entity.position.y - 8, 16, 16),
            )
