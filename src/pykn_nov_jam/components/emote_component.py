import pykraken as kn
from pykn_nov_jam.components.component import Component
from pykn_nov_jam.components.sprite_component import SpriteComponent
from pykn_nov_jam.entities.entity import Entity


class EmoteComponenet(Component):
    def __init__(self, entity: Entity, sprite_component: SpriteComponent):
        super().__init__(entity)
        self.sprite_component = sprite_component
        self.current_emote: str | None = None
