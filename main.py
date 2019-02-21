import abc
import collections
from enum import Enum, auto
import random


class AutoName(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name


class Animal(AutoName):
    RABBIT = auto()
    SHEEP = auto()
    PIG = auto()
    COW = auto()
    HORSE = auto()

    SMALL_DOG = auto()
    BIG_DOG = auto()

    FOX = auto()
    WOLF = auto()

    @staticmethod
    def get_farm_animals():
        return [Animal.RABBIT, Animal.SHEEP, Animal.PIG, Animal.COW, Animal.HORSE]


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
        animals = Animal.get_farm_animals()
        for animal in animals:
            self.animals[animal] = 0

    def breed_animals(self, dice_animals: list):
        counter = collections.Counter(dice_animals)
        for animal, amount in counter.items():
            bred_animals = Breeder.count_new_animals(self.animals[animal], amount)
            self.animals[animal] += bred_animals

    def print_state(self):
        print(self.animals)


class Dice:
    def __init__(self, animals: list):
        self.animals = animals

    def _get_side_animal_by_idx(self, side: int):
        return None if (side > len(self.animals) - 1 or len(self.animals) == 0) else self.animals[side]

    def throw(self) -> Animal:
        return self._get_side_animal_by_idx(random.randint(0, len(self.animals) - 1))


class TradeRule:
    def __init__(self, a1, a2, price):
        self.a1 = a1
        self.a2 = a2
        self.price = price

    def is_both_present(self, a1, a2):
        return (a1 == self.a1 and a2 == self.a2) or (a1 == self.a2 and a2 == self.a1)

    def get_multiplier(self, a1, a2):
        return self.price if a1 == self.a1 and a2 == self.a2 else 1 / self.price


class Trade:
    def __init__(self, trade_rules):
        self.trade_rules = trade_rules

    def is_trade_possible(self, sold_animal: Animal, bought_animal: Animal, total_available: int,
                          desired_amount: int) -> bool:
        def _get_matching_rule(_sold_animal, _bought_animal):
            for rule in self.trade_rules:
                if rule.is_both_present(_sold_animal, _bought_animal):
                    return rule
            return None

        matching_rule = _get_matching_rule(sold_animal, bought_animal)
        return False if matching_rule is None else total_available / matching_rule.get_multiplier(sold_animal,
                                                                                                  bought_animal) >= desired_amount


# TODO: Command design pattern might be a good suit for Turn and TurnHandler
class Turn:
    def __init__(self, action, previous_turn=None):
        self.action = action
        self.previous_turn = previous_turn


class TurnHandler:
    def __init__(self):
        self.turns = []
        self.options = {1: 'Roll dices',
                        2: 'Trade',
                        3: 'Exit'}

    def resolve_turn(self):
        self.print_possibilities()
        option = self.pick_option()

    def print_possibilities(self):
        print(f'Which option do you choose?')
        for key, value in self.options.items():
            print(f'{key}. {value}')

    def pick_option(self):
        return input()


if __name__ == '__main__':
    farm = Farm()
    animals = list(Animal)[:-4]
    dices = [Dice(list(Animal)[:-4] + [Animal.FOX]), Dice(list(Animal)[:-4] + [Animal.WOLF])]


    def _roll_dices():
        animals = [dice.throw() for dice in dices]
        print(f'You threw: {animals}')
        farm.breed_animals(animals)
        farm.print_state()


    options = {1: 'Roll dices',
               2: 'Trade',
               3: 'Exit'}
    keys = list(options.keys())
    # First turn
    print(f'Which option do you choose?')
    for key, value in options.items():
        print(f'{key}. {value}')
    option = int(input())
    print(f'You chose option: {option}')
    if option == 1:
        _roll_dices()
    # Other turns
    while option in keys[:-1]:
        print(f'Which option do you choose?')
        for key, value in options.items():
            print(f'{key}. {value}')
        option = int(input())
        print(f'You chose option: {option}')
        if option == 1:
            _roll_dices()
