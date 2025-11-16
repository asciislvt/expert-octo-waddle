from typing import Callable, override
import pykraken as kn
from pykn_nov_jam.components.component import Component
from pykn_nov_jam.entities.entity import Entity


class CollisionComponent(Component):
    def __init__(
        self,
        entity: Entity,
        collider: kn.Rect | None = None,
        body_type: str = "dynamic",
        on_collide: Callable[..., None] | None = None,
    ) -> None:
        super().__init__(entity)
        self.body_type: str = body_type
        if collider is None:
            # print("%s entity has no collider, creating default collider." % entity)
            self.collider: kn.Rect = kn.Rect()
        else:
            self.collider = collider
        if on_collide is None:
            # print("%s entity has no collide callback, defining empty callback" % entity)
            self.on_collide: Callable[..., None] = lambda a, b: None
        else:
            self.on_collide = on_collide

    def get_collision_direction(self, other: "CollisionComponent") -> kn.Vec2:
        return kn.Vec2()

    @override
    def process_update(self, delta_time: float) -> None:
        if self.enabled is False:
            return

        self.collider.x = self.entity.position.x - (self.collider.w / 2)
        self.collider.y = self.entity.position.y - (self.collider.h / 2)

    # NOTE: Just for debugging ;3
    @override
    def process_draw(self) -> None:
        kn.draw.rect(self.collider, kn.Color(100, 255, 200, 200))
        # pass

    def get_collider(self) -> kn.Rect:
        return self.collider
