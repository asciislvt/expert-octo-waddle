import pykraken as kn

from pykn_nov_jam.entities.entity_manager import EntityManager


class EmoteSystem:
    def __init__(self, entity_manager: EntityManager) -> None:
        self.entity_manager = entity_manager
        self.emote_atlas: kn.Texture = kn.Texture("assets/sprites/emotes.png")
        self.emotes = {
            "follow": kn.Rect(0, 0, 8, 8),
            "flee": kn.Rect(0, 8, 8, 8),
            "whistle": kn.Rect(8, 0, 8, 8),
            "hungry": kn.Rect(16, 0, 8, 8),
            "satisfied": kn.Rect(16, 8, 8, 8),
        }

    def get_emote_rect(self, emote_name: str) -> kn.Rect:
        return self.emotes.get(emote_name, kn.Rect(0, 0, 8, 8))
