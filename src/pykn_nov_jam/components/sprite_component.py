from typing import override
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
        offset_x: int = 8,
        offset_y: int = 8,
        source_rect: kn.Rect | None = None,
    ) -> None:
        super().__init__(entity)
        self.sprite_path: str | None = sprite_path
        self.sprite: kn.Texture | None = None
        self.width: int = width
        self.height: int = height
        self.offset_x: int = offset_x
        self.offset_y: int = offset_y
        self.source_rect: kn.Rect | None = source_rect
        self.load_sprite()

    def set_source_rect(self, new_rect: kn.Rect) -> None:
        self.source_rect = new_rect

    def offset_source_rect(self, offset_x: int, offset_y: int) -> None:
        if self.source_rect is None:
            print("No source rect to offset.")
            return

        self.source_rect.x = offset_x
        self.source_rect.y = offset_y

    def load_sprite(self) -> None:
        if self.sprite_path is None:
            print("No sprite path provided, using placeholder rectangle.")
            return
        else:
            self.sprite = kn.Texture(self.sprite_path)

    @override
    def process_draw(self) -> None:
        if self.enabled is False:
            return

        if self.sprite is None:
            print("No sprite loaded.")
            # kn.draw.rect(
            #     kn.Rect(
            #         self.entity.position.x - self.width / 2,
            #         self.entity.position.y - self.height / 2,
            #         self.width,
            #         self.height,
            #     ),
            #     kn.Color(0, 255, 0),
            # )
        else:
            kn.renderer.draw(
                self.sprite,
                kn.Rect(
                    self.entity.position.x - self.offset_x,
                    self.entity.position.y - self.offset_y,
                    self.width,
                    self.height,
                ),
                self.source_rect,
            )
