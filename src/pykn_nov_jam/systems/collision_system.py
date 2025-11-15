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

        for entity in entity_list:
            collision_comp: CollisionComponent = entity.get_component(
                CollisionComponent
            )  # type: ignore

            collider = collision_comp.get_collider()
            cell_pos = SpatialHash._instance.get_cell_position(entity.position)
            nearby_entities = SpatialHash._instance.get_nearby_entities(cell_pos)

            for other_entity in nearby_entities:
                if other_entity == entity:
                    continue

                other_collision_comp: CollisionComponent = other_entity.get_component(  # type: ignore
                    CollisionComponent
                )

                other_collider = other_collision_comp.get_collider()

                if self.check_collision(collider, other_collider):
                    self.handle_collision(entity, other_entity)

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
            self.push_entities_apart(entity_a, entity_b)

        if collision_a.on_collide is not None:
            collision_a.on_collide(entity_a, entity_b)
        if collision_b.on_collide is not None:
            collision_b.on_collide(entity_b, entity_a)

    def check_collision(self, rect_1: kn.Rect, rect_2: kn.Rect) -> bool:
        if (
            rect_1.x < rect_2.x + rect_2.w
            and rect_1.x + rect_1.w > rect_2.x
            and rect_1.y < rect_2.y + rect_2.h
            and rect_1.y + rect_1.h > rect_2.y
        ):
            return True

        return False

    def push_entities_apart(self, entity_a: Entity, entity_b: Entity) -> None:
        movement_a: MovementComponent | None = entity_a.get_component(  # type: ignore
            MovementComponent
        )
        movement_b: MovementComponent | None = entity_b.get_component(  # type: ignore
            MovementComponent
        )

        if movement_a is not None:
            movement_a.velocity = kn.Vec2(0, 0)
        if movement_b is not None:
            movement_b.velocity = kn.Vec2(0, 0)
