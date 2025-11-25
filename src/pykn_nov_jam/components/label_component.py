import pykraken as kn

from pykn_nov_jam.components.component import Component
from pykn_nov_jam.entities.entity import Entity


class LabelComponent(Component):
    def __init__(
        self,
        entity: Entity,
        text: str = "test string",
        color: kn.Color = kn.color.RED,
        offset: kn.Vec2 = kn.Vec2(0, 0),
        size: int = 8,
        visible: bool = False,
    ):
        super().__init__(entity)
        self.text: str = text
        self.color: kn.Color = color
        self.offset: kn.Vec2 = offset
        self.size: int = size
        self.visible: bool = visible
        self.font: kn.Font = kn.Font("kraken-retro", size)
        self.text_object: kn.Text = kn.Text(self.font)
        self.text_object.text = self.text

    def process_draw(self) -> None:
        if self.visible:
            padding = 2
            text_rect = self.text_object.get_rect()
            text_rect.w += padding * 2
            text_rect.h += padding
            text_rect.x = (self.entity.position.x + self.offset.x) - padding
            text_rect.y = (self.entity.position.y + self.offset.y) - padding
            kn.draw.rect(text_rect, kn.color.DARK_GRAY)
            self.text_object.draw(self.entity.position + self.offset)
