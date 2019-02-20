import abc
from enum import Enum, auto
import random


class AutoName(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name


class Animal(AutoName):
    RABBIT = auto()
    SHEEP = auto()
    SMALL_DOG = auto()
    PIG = auto()
    COW = auto()
    BIG_DOG = auto()
    HORSE = auto()
    FOX = auto()
    WOLF = auto()


class Breeder:
    @staticmethod
    def count_new_animals(present_animals, animals_on_sides) -> int:
        return 0 if animals_on_sides == 0 else int((present_animals + animals_on_sides) / 2)


class Farm:
    def __init__(self):
        self.animals = [0, 0, 0]

    def breed_animals(self, dice_animals):
        new_animals = [Breeder.count_new_animals(ex, dice) for ex, dice in zip(self.animals, dice_animals)]
        for i, to_add in enumerate(new_animals):
            self.animals[i] += to_add


class Dice:
    def __init__(self, animals: list):
        self.animals = animals

    def _get_side_animal_by_idx(self, side: int):
        return None if (side > len(self.animals) - 1 or len(self.animals) == 0) else self.animals[side]

    def throw(self) -> Animal:
        return self._get_side_animal_by_idx(random.randint(0, len(self.animals) - 1))


class Trade:
    def __init__(self, trade_rules):
        self.trade_rules = trade_rules

    def is_trade_possible(self, sold_animal: Animal, bought_animal: Animal, total_available: int,
                          desired_amount: int) -> bool:
        for rule in self.trade_rules:
            if bought_animal in rule and sold_animal in rule:
                return total_available / rule[2] >= desired_amount
        return False
