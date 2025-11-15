import pykraken as kn
from pykn_nov_jam.components.component import Component
from pykn_nov_jam.entities.entity import Entity


class SpriteComponent(Component):
    def __init__(
        self,
        entity: Entity,
        sprite_path: str | None = None,
        width: int = 16,
        height: int = 16,
    ) -> None:
        super().__init__(entity)
        self.sprite_path: str | None = sprite_path
        self.sprite: kn.Texture | None = None
        self.width: int = width
        self.height: int = height
        self.load_sprite()

    def load_sprite(self) -> None:
        if self.sprite_path is None:
            print("No sprite path provided, using placeholder rectangle.")
            return
        else:
            self.sprite = kn.Texture(self.sprite_path)

    def process_draw(self) -> None:
        if self.enabled is False:
            return

        if self.sprite is None:
            kn.draw.rect(
                kn.Rect(
                    self.entity.position.x - 8,
                    self.entity.position.y - 8,
                    self.width,
                    self.height,
                ),
                kn.Color(0, 255, 0),
            )
        else:
            kn.renderer.draw(
                self.sprite,
                kn.Rect(
                    self.entity.position.x - 8,
                    self.entity.position.y - 8,
                    self.width,
                    self.height,
                ),
            )
