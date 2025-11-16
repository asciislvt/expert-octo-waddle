import pykraken as kn
import math
from pykn_nov_jam.components.collision_component import CollisionComponent
from pykn_nov_jam.entities.entity import Entity


class SpatialHash:
    _instance: "SpatialHash | None" = None

    def __init__(self, cell_size: int = 32):
        SpatialHash._instance = self
        self.cell_size: int = cell_size
        self.cells: dict[kn.Vec2, list[Entity]] = {}
        print("SpatialHash initialized")

    def clear(self) -> None:
        self.cells.clear()

    def insert(self, entity: Entity) -> None:
        cell_ids = self.get_cell_ids(entity)

        for cell_id in cell_ids:
            print("Inserting entity %r into cell %r" % (entity, cell_id))
            if cell_id not in self.cells.keys():
                self.cells[cell_id] = []
            self.cells[cell_id].append(entity)

    def get_cells(self) -> dict[kn.Vec2, list[Entity]]:
        return self.cells

    def get_nearby_entities(self, cell_position: kn.Vec2) -> list[Entity]:
        result: list[Entity] = []
        neighbor_cells = self.get_neighbor_cells(cell_position)

        for cell in neighbor_cells:
            for entity in self.cells[cell]:
                result.append(entity)

        return result

    def get_neighbor_cells(self, cell_position: kn.Vec2) -> list[kn.Vec2]:
        result: list[kn.Vec2] = []
        for x in range(-1, 2):
            for y in range(-1, 2):
                neighbor_cell = kn.Vec2(cell_position.x + x, cell_position.y + y)
                if neighbor_cell == cell_position:
                    continue
                if neighbor_cell in self.cells:
                    result.append(neighbor_cell)

        return result

    def get_cell_ids(self, entity: Entity) -> list[kn.Vec2]:
        cell_ids: list[kn.Vec2] = []
        entity_collider: CollisionComponent | None = entity.get_component(
            CollisionComponent
        )  # type: ignore
        if entity_collider is None:
            print(
                "SpatialHash: Entity %r has no CollisionComponent, cannot get cell IDs."
                % entity
            )
            return cell_ids

        positions_to_check = []
        width_steps = math.ceil(entity_collider.collider.w / self.cell_size)
        height_steps = math.ceil(entity_collider.collider.h / self.cell_size)

        for w in range(width_steps + 1):
            for h in range(height_steps + 1):
                step_x = w * self.cell_size
                step_y = h * self.cell_size
                position = kn.Vec2(
                    step_x + entity_collider.collider.x,
                    step_y + entity_collider.collider.y,
                )
                positions_to_check.append(position)

        for position in positions_to_check:
            cell_pos = self.get_cell_position(position)
            if cell_pos not in cell_ids:
                cell_ids.append(cell_pos)

        return cell_ids

    def get_cell_position(self, position: kn.Vec2) -> kn.Vec2:
        cell_x = math.floor(position.x / self.cell_size)
        cell_y = math.floor(position.y / self.cell_size)
        return kn.Vec2(cell_x, cell_y)

    def debug_draw_cells(self) -> None:
        for cell_position in self.cells.keys():
            cell_rect = kn.Rect(
                cell_position.x * self.cell_size,
                cell_position.y * self.cell_size,
                self.cell_size,
                self.cell_size,
            )
            kn.draw.rect(cell_rect, kn.Color(255, 0, 0, 100), False)
