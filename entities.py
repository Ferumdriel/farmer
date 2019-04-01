import collections
import random
from enum import Enum, auto


class AutoName(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name

    def __repr__(self):
        return self.name


class AnimalState:
    def __init__(self, name, value, friendly):
        self.name = name
        self.value = value
        self.friendly = friendly


class AnimalType(AutoName):
    RABBIT = AnimalState(auto(), 1, True)
    SHEEP = AnimalState(auto(), 6, True)
    PIG = AnimalState(auto(), 12, True)
    COW = AnimalState(auto(), 36, True)
    HORSE = AnimalState(auto(), 72, True)

    SMALL_DOG = AnimalState(auto(), 6, True)
    BIG_DOG = AnimalState(auto(), 36, True)

    FOX = AnimalState(auto(), 0, False)
    WOLF = AnimalState(auto(), 0, False)

    def is_tradeable(self):
        return self.value.friendly

    def get_value(self):
        return self.value.value

    @staticmethod
    def get_farm_animals():
        return [AnimalType.RABBIT, AnimalType.SHEEP, AnimalType.PIG, AnimalType.COW, AnimalType.HORSE]

class Breeder:
    @staticmethod
    def count_new_animals(present_animals: int, animals_on_sides: int) -> int:
        return 0 if animals_on_sides == 0 else int((present_animals + animals_on_sides) / 2)


class Farm:
    def __init__(self, animals=None):
        self.animals = animals
        if self.animals is None:
            self._initialize_animals()

    def _initialize_animals(self):
        self.animals = {}
        animals = AnimalType.get_farm_animals()
        for animal in animals:
            self.animals[animal] = 0

    def breed_animals(self, dice_animals: list):
        counter = collections.Counter(dice_animals)
        if AnimalType.FOX in counter:
            del counter[AnimalType.RABBIT]
        if AnimalType.WOLF in counter:
            counter = collections.Counter([AnimalType.WOLF])
        for animal, amount in counter.items():
            try:
                bred_animals = Breeder.count_new_animals(self.animals[animal], amount)
                self.animals[animal] += bred_animals
            except KeyError:
                if animal == AnimalType.FOX:
                    print('Oh no! Fox ate all your rabbits!')
                    self.animals[AnimalType.RABBIT] = 0
                elif animal == AnimalType.WOLF:
                    print('Oh no! Wolf ate everything except horses!')
                    for farm_animal in self.animals.keys():
                        if farm_animal != AnimalType.HORSE:
                            self.animals[farm_animal] = 0

    def print_state(self):
        print(self.animals)


class Dice:
    def __init__(self, animals_on_sides: list):
        self.animals_on_sides = animals_on_sides
        self.result = None

    def _get_side_animal_by_idx(self, side: int):
        return None if (side > len(self.animals_on_sides) - 1 or len(self.animals_on_sides) == 0) else \
            self.animals_on_sides[side]

    def throw(self) -> AnimalType:
        return self._get_side_animal_by_idx(random.randint(0, len(self.animals_on_sides) - 1))
