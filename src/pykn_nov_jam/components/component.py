class Component:
    def __init__(self, entity):
        self.entity = entity

    def process_update(self, delta_time: float):
        pass

    def process_input(self):
        pass

    def process_draw(self):
        pass
