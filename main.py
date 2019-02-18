import abc
import enum
import random

class Animal(enum.Enum):
    RABBIT = 1
    SHEEP = RABBIT.value * 6
    SMALL_DOG = SHEEP.value
    PIG = SHEEP.value * 2
    COW = PIG.value * 3
    BIG_DOG = COW.value
    HORSE = COW.value * 2
    FOX = 0
    WOLF = 0


class Dice:
    def __init__(self, animals: list):
        self.animals = animals

    def _get_side_animal(self, side: int):
        return self.animals[side]

    def throw(self):
        return self._get_side_animal(random.randint(0, len(self.animals) - 1))
