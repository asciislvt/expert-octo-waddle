import pykraken as kn
from entities.entity_manager import EntityManager
from systems.system import System


class MovementSystem(System):
    def __init__(self):
        pass

    def process_components(self, entity, delta_time):

