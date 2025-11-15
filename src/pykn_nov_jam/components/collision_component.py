import pykraken as kn
from components.component import Component
from entities.entity import Entity


class CollisionComponent(Component):
    def __init__(self, entity: Entity, collider: kn.Rect | None = None) -> None:
        super().__init__(entity)
        if collider is None:
            print("%s entity has no collider, creating default collider." % entity)
            self.collider: kn.Rect = kn.Rect()
        else:
            self.collider = collider
        # print(
        #     "CollisionComponent created for entity %s with collider %r"
        #     % (entity, self.collider)
        # )

    def process_update(self, delta_time: float) -> None:
        if self.enabled is False:
            return

        self.collider.x = self.entity.position.x - 8
        self.collider.y = self.entity.position.y - 8

    # NOTE: Just for debugging ;3
    def process_draw(self) -> None:
        kn.draw.rect(self.collider, kn.Color(100, 255, 200, 200))

    def get_collider(self) -> kn.Rect:
        return self.collider
