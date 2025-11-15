import pykraken as kn
from pykn_nov_jam.entities.entity import Entity


class SpatialHash:
    _instance: "SpatialHash | None" = None

    def __init__(self, cell_size: int = 16):
        self.cell_size: int = cell_size
        self.cells: dict[kn.Vec2, list[Entity]] = {}
        SpatialHash._instance = self
        print("SpatialHash initialized")

    def clear(self) -> None:
        self.cells.clear()

    def insert(self, entity: Entity) -> None:
        cell_pos = self.get_cell_position(entity.position)
        if cell_pos not in self.cells:
            self.cells[cell_pos] = []

        self.cells[cell_pos].append(entity)

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
                # if neighbor_cell == cell_position:
                #     continue
                if neighbor_cell in self.cells:
                    result.append(neighbor_cell)

        return result

    def get_cell_position(self, position: kn.Vec2) -> kn.Vec2:
        cell_x = int(position.x) // self.cell_size
        cell_y = int(position.y) // self.cell_size
        return kn.Vec2(cell_x, cell_y)
