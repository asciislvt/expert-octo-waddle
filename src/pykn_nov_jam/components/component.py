class Component:
    def __init__(self, entity) -> None:
        self.entity = entity

    def process_update(self, delta_time: float) -> None:
        pass

    def process_input(self) -> None:
        pass

    def process_draw(self) -> None:
        pass
