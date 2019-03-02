import abc
import collections
from enum import Enum, auto
import random


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

    def _get_side_animal_by_idx(self, side: int):
        return None if (side > len(self.animals_on_sides) - 1 or len(self.animals_on_sides) == 0) else self.animals_on_sides[side]

    def throw(self) -> AnimalType:
        return self._get_side_animal_by_idx(random.randint(0, len(self.animals_on_sides) - 1))

class Trade:
    def trade(self, sold_animal: AnimalType, bought_animal: AnimalType, farm: Farm, desired_amount: int):
        if self.is_trade_possible(sold_animal, bought_animal, farm.animals[sold_animal], desired_amount):
            multiplier = self.get_multiplier(sold_animal, bought_animal)
            farm.animals[sold_animal] -= desired_amount * multiplier
            farm.animals[bought_animal] += desired_amount

    def is_trade_possible(self, sold_animal: AnimalType, bought_animal: AnimalType, total_available: int,
                          desired_amount: int) -> bool:
        if sold_animal.is_tradeable() and bought_animal.is_tradeable() and sold_animal != bought_animal:
            return total_available / self.get_multiplier(sold_animal, bought_animal) >= desired_amount
        return False

    def get_multiplier(self, sold_animal: AnimalType, bought_animal: AnimalType):
        value1 = sold_animal.get_value()
        value2 = bought_animal.get_value()
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
        self.dices = [
            Dice(6 * [AnimalType.RABBIT] + 3 * [AnimalType.SHEEP] + [AnimalType.PIG, AnimalType.COW, AnimalType.WOLF]),
            Dice(6 * [AnimalType.RABBIT] + 2 * [AnimalType.SHEEP, AnimalType.PIG] + [AnimalType.HORSE, AnimalType.FOX])]
        self.options = {1: 'Roll dices',
                        2: 'Trade',
                        3: 'Exit'}
        # FIXME Some variable to check if animal is tradeable might be better
        self.trade = Trade()

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
