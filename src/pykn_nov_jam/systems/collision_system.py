import pykraken as kn
from components.collision_component import CollisionComponent
from entities.entity_manager import EntityManager
from systems.system import System
from spatial_hash import SpatialHash


class CollisionSystem(System):
    def __init__(self):
        pass

    def process_components(self, delta_time: float) -> None:
        if EntityManager._instance is None or SpatialHash._instance is None:
            print("CollisionSystem: EntityManager or SpatialHash not initialized.")
            return
        else:
            for entity in EntityManager._instance.get_entities_with_component(
                CollisionComponent
            ):
                SpatialHash._instance.insert(entity)

            for entity in EntityManager._instance.get_entities_with_component(
                CollisionComponent
            ):
                collision_comp: CollisionComponent = entity.get_component(
                    CollisionComponent
                )  # type: ignore

                collider = collision_comp.collider
                cell_pos = SpatialHash._instance.get_cell_position(entity.position)
                nearby_entities = SpatialHash._instance.get_nearby_entities(cell_pos)

                for other_entity in nearby_entities:
                    if other_entity == entity:
                        continue

                    other_collision_comp: CollisionComponent = (
                        other_entity.get_component(  # type: ignore
                            CollisionComponent
                        )
                    )
                    if other_collision_comp is None:
                        continue

                    other_collider = other_collision_comp.get_collider()

                    if self.check_collision(collider, other_collider):
                        print(
                            "Collision detected between %s and %s"
                            % (entity, other_entity)
                        )

    def check_collision(self, rect_1: kn.Rect, rect_2: kn.Rect) -> bool:
        if (
            rect_1.x < rect_2.x + rect_2.w
            and rect_1.x + rect_1.w > rect_2.x
            and rect_1.y < rect_2.y + rect_2.h
            and rect_1.y + rect_1.h > rect_2.y
        ):
            return True

        return False
