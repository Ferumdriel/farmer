import abc
import enum
import random


# class Animal(enum.Enum):
#     RABBIT = 1
#     SHEEP = RABBIT.value * 6
#     SMALL_DOG = SHEEP.value
#     PIG = SHEEP.value * 2
#     COW = PIG.value * 3
#     BIG_DOG = COW.value
#     HORSE = COW.value * 2
#     FOX = 0
#     WOLF = 0


class Breeder:
    @staticmethod
    def count_new_animals(present_animals, animals_on_sides):
        return 0 if animals_on_sides == 0 else int((present_animals + animals_on_sides) / 2)

class Farm:
    def __init__(self):
        self.animals = [0,0,0]

    def breed_animals(self, dice_animals):
        new_animals = [Breeder.count_new_animals(ex, dice) for ex, dice in zip(self.animals, dice_animals)]
        for i, to_add in enumerate(new_animals):
            self.animals[i] += to_add



class Dice:
    def __init__(self, animals: list):
        self.animals = animals

    def _get_side_animal(self, side: int):
        return self.animals[side]

    def throw(self):
        return self._get_side_animal(random.randint(0, len(self.animals) - 1))
