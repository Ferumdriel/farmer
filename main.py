import abc
import collections
from enum import Enum, auto
import random


class AutoName(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name

    def __repr__(self):
        return self.name


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
        if Animal.FOX in counter:
            del counter[Animal.RABBIT]
        if Animal.WOLF in counter:
            counter = collections.Counter([Animal.WOLF])
        for animal, amount in counter.items():
            try:
                bred_animals = Breeder.count_new_animals(self.animals[animal], amount)
                self.animals[animal] += bred_animals
            except KeyError:
                if animal == Animal.FOX:
                    print('Oh no! Fox ate all your rabbits!')
                    self.animals[Animal.RABBIT] = 0
                elif animal == Animal.WOLF:
                    print('Oh no! Wolf ate everything except horses!')
                    for farm_animal in self.animals.keys():
                        if farm_animal != Animal.HORSE:
                            self.animals[farm_animal] = 0

    def print_state(self):
        print(self.animals)


class Dice:
    def __init__(self, animals: list):
        self.animals = animals

    def _get_side_animal_by_idx(self, side: int):
        return None if (side > len(self.animals) - 1 or len(self.animals) == 0) else self.animals[side]

    def throw(self) -> Animal:
        return self._get_side_animal_by_idx(random.randint(0, len(self.animals) - 1))


class TradeValues:
    def __init__(self):
        self.values = {Animal.RABBIT: 1}
        self.values[Animal.SHEEP] = self.values[Animal.RABBIT] * 6
        self.values[Animal.PIG] = self.values[Animal.SHEEP] * 2
        self.values[Animal.COW] = self.values[Animal.PIG] * 3
        self.values[Animal.HORSE] = self.values[Animal.COW] * 2
        self.values[Animal.SMALL_DOG] = self.values[Animal.RABBIT] * 6
        self.values[Animal.BIG_DOG] = self.values[Animal.COW]

    def get_value(self, animal: Animal):
        value = 0
        try:
            value = self.values[animal]
        except KeyError:
            print(f'Key {animal} does not exist.')
        return value


class TradeRule:
    def __init__(self, a1: Animal, a2: Animal):
        self.a1 = a1
        self.a2 = a2

    def is_both_present(self, a1, a2):
        return (a1 == self.a1 and a2 == self.a2) or (a1 == self.a2 and a2 == self.a1)



class Trade:
    def __init__(self, trade_rules):
        self.trade_rules = trade_rules
        self.trade_values = TradeValues()

    def trade(self, sold_animal: Animal, bought_animal: Animal, farm: Farm, desired_amount: int):
        if self.is_trade_possible(sold_animal, bought_animal, farm.animals[sold_animal], desired_amount):
            multiplier = self.get_multiplier(sold_animal, bought_animal)
            farm.animals[sold_animal] -= desired_amount * multiplier
            farm.animals[bought_animal] += desired_amount

    def is_trade_possible(self, sold_animal: Animal, bought_animal: Animal, total_available: int,
                          desired_amount: int) -> bool:
        if self.get_matching_rule(sold_animal, bought_animal) is None:
            return False
        return total_available / self.get_multiplier(sold_animal,bought_animal) >= desired_amount

    def get_matching_rule(self, a1: Animal, a2: Animal) -> TradeRule:
        for rule in self.trade_rules:
            if rule.is_both_present(a1, a2):
                return rule
        return None

    def get_multiplier(self, sold_animal: Animal, bought_animal: Animal):
        value1 = self.trade_values.get_value(sold_animal)
        value2 = self.trade_values.get_value(bought_animal)
        return value2 if value1 < value2 else 1 / value1


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


class Game:
    def __init__(self):
        self.farm = Farm()
        self.dices = [Dice(6 * [Animal.RABBIT] + 3 * [Animal.SHEEP] + [Animal.PIG, Animal.COW, Animal.WOLF]),
                      Dice(6 * [Animal.RABBIT] + 2 * [Animal.SHEEP, Animal.PIG] + [Animal.HORSE, Animal.FOX])]
        self.options = {1: 'Roll dices',
                        2: 'Trade',
                        3: 'Exit'}
        # FIXME Some variable to check if animal is tradeable might be better
        self.trade = Trade([TradeRule(Animal.RABBIT, Animal.SHEEP)] )

    def resolve_turn(self):
        def _roll_dices():
            animals = [dice.throw() for dice in self.dices]
            print(f'You threw: {animals}')
            self.farm.breed_animals(animals)
            self.farm.print_state()

        self.print_options()
        option = int(input('Enter value: '))
        if option == 1:
            _roll_dices()
        return option

    def print_options(self):
        print('Which option do you choose?')
        print(self.options_txt)

    @property
    def options_txt(self):
        opt_text = ''
        for key, value in self.options.items():
            opt_text += f'{key}. {value}\n'
        return opt_text

    def main_loop(self):
        option = self.resolve_turn()
        while option in list(self.options.keys())[:-1]:
            option = self.resolve_turn()


if __name__ == '__main__':
    game = Game()
    game.main_loop()
