import pykraken as kn

from pykn_nov_jam.components.collision_component import CollisionComponent
from pykn_nov_jam.entities.entity import Entity
from pykn_nov_jam.entities.entity_manager import EntityManager
from pykn_nov_jam.spatial_hash import SpatialHash


class CollisionSystem:
    # _instance: "CollisionSystem | None" = None
    prediction_steps: int = 3

    def __init__(
        self,
        prediction_steps: int = 3,
        entity_manager: EntityManager | None = None,
        spatial_hash: SpatialHash | None = None,
    ) -> None:
        CollisionSystem._instance = self
        self.entity_manager = entity_manager
        self.spatial_hash = spatial_hash
        CollisionSystem.prediction_steps = prediction_steps
        if self.entity_manager is None:
            print("CollisionSystem: EntityManager not provided.")
        if self.spatial_hash is None:
            print("CollisionSystem: SpatialHash not provided.")
        print("CollisionSystem initialized")

    def process_collisions(self, delta_time: float) -> None:
        if self.entity_manager is None or self.spatial_hash is None:
            print("CollisionSystem: EntityManager or SpatialHash not initialized.")
            return
        self.spatial_hash.clear()
        entity_list = self.entity_manager.get_entities_with_component(
            CollisionComponent
        )

        for entity in entity_list:
            self.spatial_hash.insert(entity)

        cells = self.spatial_hash.get_cells()
        for cell_position in cells.keys():
            cell_list = cells[cell_position]
            if len(cell_list) < 2:
                # print("Cell has less than 2 entities, skipping collision checks.")
                continue

            for entity_a in cells[cell_position]:
                for entity_b in cells[cell_position]:
                    if entity_a == entity_b:
                        continue
                    if cell_list.index(entity_a) >= cell_list.index(entity_b):
                        continue

                    collision_a: CollisionComponent = entity_a.get_component(
                        CollisionComponent
                    )  # type: ignore
                    collision_b: CollisionComponent = entity_b.get_component(
                        CollisionComponent
                    )  # type: ignore

                    if self.is_colliding(
                        collision_a.get_collider(), collision_b.get_collider()
                    ):
                        self.handle_collision(entity_a, entity_b)

    def predict_collision(
        self, entity: Entity, target_position: kn.Vec2
    ) -> tuple[bool, kn.Vec2]:
        if self.spatial_hash is None:
            print("CollisionSystem: SpatialHash not initialized.")
            return (False, kn.Vec2(0, 0))

        neighbors = self.spatial_hash.get_neighbor_entities(entity)
        if len(neighbors) == 0:
            return (False, kn.Vec2(0, 0))

        for neighbor in neighbors:
            neighbor_collision: CollisionComponent = neighbor.get_component(  # type: ignore
                CollisionComponent
            )
            collision_component: CollisionComponent = entity.get_component(  # type: ignore
                CollisionComponent
            )

            neighbor_collider: kn.Rect = neighbor_collision.get_collider()
            collider = collision_component.get_collider().copy()
            collider.x = target_position.x - (collider.w / 2)
            collider.y = target_position.y - (collider.h / 2)

            if self.is_colliding(collider, neighbor_collider):
                normal = self.get_collision_direction(collider, neighbor_collider)
                normal.normalize()
                return (True, normal)

        return (False, kn.Vec2(0, 0))

    def is_colliding(self, rect_1: kn.Rect, rect_2: kn.Rect) -> bool:
        if (
            rect_1.left < rect_2.right
            and rect_1.right > rect_2.left
            and rect_1.top < rect_2.bottom
            and rect_1.bottom > rect_2.top
        ):
            return True

        return False

    def handle_collision(self, entity_a: Entity, entity_b: Entity) -> None:
        collision_a: CollisionComponent = entity_a.get_component(  # type: ignore
            CollisionComponent
        )
        collision_b: CollisionComponent = entity_b.get_component(  # type: ignore
            CollisionComponent
        )

        if collision_a.body_type == "static" and collision_b.body_type == "static":
            return
        if collision_a.body_type == "dynamic" and collision_b.body_type == "static":
            self.resolve_collision(entity_a, entity_b)
            return
        if collision_a.body_type == "static" and collision_b.body_type == "dynamic":
            self.resolve_collision(entity_b, entity_a)
            return

        # TODO: Implement collision callbacks
        #
        # if collision_a.on_collide is not None:
        #     collision_a.on_collide(entity_a, entity_b)
        # if collision_b.on_collide is not None:
        #     collision_b.on_collide(entity_b, entity_a)

    def resolve_collision(self, entity_a: Entity, entity_b: Entity) -> None:
        collision_a: CollisionComponent = entity_a.get_component(  # type: ignore
            CollisionComponent
        )
        collision_b: CollisionComponent = entity_b.get_component(  # type: ignore
            CollisionComponent
        )

        rect_a = collision_a.get_collider()
        rect_b = collision_b.get_collider()

        resolve_vector = self.get_collision_direction(rect_a, rect_b)
        entity_a.position += resolve_vector

    def get_collision_direction(self, rect_a: kn.Rect, rect_b: kn.Rect) -> kn.Vec2:
        diff_x = min(rect_a.right, rect_b.right) - max(rect_a.left, rect_b.left)
        diff_y = min(rect_a.bottom, rect_b.bottom) - max(rect_a.top, rect_b.top)

        margin = 0.0001
        resolve_vector = kn.Vec2(0, 0)
        if diff_x < diff_y:
            if rect_a.center.x < rect_b.center.x:
                resolve_vector.x = -(diff_x + margin)
            else:
                resolve_vector.x = diff_x + margin
        else:
            if rect_a.center.y < rect_b.center.y:
                resolve_vector.y = -(diff_y + margin)
            else:
                resolve_vector.y = diff_y + margin

        return resolve_vector
