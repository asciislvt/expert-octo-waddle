import pykraken as kn
from pykn_nov_jam.components.collision_component import CollisionComponent
from pykn_nov_jam.components.movement_component import MovementComponent
from pykn_nov_jam.entities.entity_manager import EntityManager
from pykn_nov_jam.entities.entity import Entity
from pykn_nov_jam.spatial_hash import SpatialHash


class CollisionSystem:
    def __init__(self):
        pass

    def process_components(self, delta_time: float) -> None:
        if EntityManager._instance is None or SpatialHash._instance is None:
            print("CollisionSystem: EntityManager or SpatialHash not initialized.")
            return
        SpatialHash._instance.clear()
        entity_list = EntityManager._instance.get_entities_with_component(
            CollisionComponent
        )

        for entity in entity_list:
            SpatialHash._instance.insert(entity)

        cells = SpatialHash._instance.get_cells()
        for cell_position in cells.keys():
            cell_list = cells[cell_position]
            if len(cell_list) < 2:
                # print("Cell has less than 2 entities, skipping collision checks.")
                continue

            for entity_a in cells[cell_position]:
                for entity_b in cells[cell_position]:
                    # print(
                    #     "---\nChecking collision between %s and %s \n Cell Position: %s\n---"
                    #     % (entity_a, entity_b, cell_position)
                    # )
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

    #                 if cell_list.index(entity_a) < cell_list.index(entity_b):
    #                     if self.check_collision(
    #                         collision_a.get_collider(), collision_b.get_collider()
    #                     ):
    #                         self.handle_collision(entity_a, entity_b)
    #                 else:
    #                     continue
    #
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
        print("Resolving collision between %s and %s" % (entity_a, entity_b))
        collision_a: CollisionComponent = entity_a.get_component(  # type: ignore
            CollisionComponent
        )
        collision_b: CollisionComponent = entity_b.get_component(  # type: ignore
            CollisionComponent
        )

        rect_a = collision_a.get_collider()
        rect_b = collision_b.get_collider()

        diff_x = min(rect_a.right, rect_b.right) - max(rect_a.left, rect_b.left)
        diff_y = min(rect_a.bottom, rect_b.bottom) - max(rect_a.top, rect_b.top)

        resolve_vector = kn.Vec2(0, 0)
        if diff_x < diff_y:
            if rect_a.center.x < rect_b.center.x:
                resolve_vector.x = -diff_x
            else:
                resolve_vector.x = diff_x
        else:
            if rect_a.center.y < rect_b.center.y:
                resolve_vector.y = -diff_y
            else:
                resolve_vector.y = diff_y

        entity_a.position += resolve_vector
