import sys
from abc import ABC, abstractmethod
from entities import AnimalType, Farm
from utils import InputListener


class Option(ABC):
    def __init__(self, display_name):
        self.display_name = display_name

    @abstractmethod
    def execute(self):
        pass

    def __str__(self):
        return self.display_name


class DiceRoller(Option):
    def __init__(self, display_name, dices, farm):
        super().__init__(display_name)
        self.dices = dices
        self.farm = farm

    def execute(self):
        animals = [dice.throw() for dice in self.dices]
        print(f'You threw: {animals}')
        self.farm.breed_animals(animals)
        self.farm.print_state()


class TradeRequest:
    def __init__(self, sold_animal: AnimalType, bought_animal: AnimalType, farm: Farm, desired_amount: int):
        self.sold_animal = sold_animal
        self.bought_animal = bought_animal
        self.farm = farm
        self.desired_amount = desired_amount

    def trade(self):
        sold, bought = 0, 0
        if self.is_trade_possible():
            multiplier = self.get_multiplier()
            sold = self.desired_amount * multiplier
            bought = self.desired_amount
            self.farm.animals[self.sold_animal] -= self.desired_amount * multiplier
            self.farm.animals[self.bought_animal] += self.desired_amount
        else:
            print('Trade is not possible.')
        return sold, bought

    def is_trade_possible(self) -> bool:
        if self.sold_animal.is_tradeable() and self.bought_animal.is_tradeable() and self.sold_animal != self.bought_animal:
            total_available = self.farm.animals[self.sold_animal]
            return total_available / self.get_multiplier() >= self.desired_amount
        return False

    def get_multiplier(self):
        value1 = self.sold_animal.get_value()
        value2 = self.bought_animal.get_value()
        return value2 if value1 < value2 else 1 / value1


class Trader(Option):
    def __init__(self, display_name, farm: Farm):
        super().__init__(display_name)
        self.farm = farm
        self._initialise_trade_options()

    def _initialise_trade_options(self):
        trade_options = {}
        for numb, animal in enumerate(list(AnimalType)):
            if animal.is_tradeable():
                trade_options[numb] = animal
                print(f'Added {animal} with number: {numb}')
            else:
                numb -= 1
            self.trade_options = trade_options

    def execute(self):
        print(f'Which animal to sell?\nAvailable options: {self.trade_options}')
        sell_animal_option = InputListener.get_int_input(0, len(self.trade_options))
        print(f'Which animal to buy?\nAvailable options: {self.trade_options}')
        buy_animal_option = InputListener.get_int_input(0, len(self.trade_options))
        print('How many animals to buy?')
        amount_to_buy = InputListener.get_int_input(1)

        trade = TradeRequest(self.trade_options[sell_animal_option], self.trade_options[buy_animal_option],
                             self.farm, amount_to_buy)
        trade.trade()
        self.farm.print_state()


class Cheatmode(Option):
    def __init__(self, display_name, farm):
        super().__init__(display_name)
        self.farm = farm

    def execute(self):
        for animal, amount in self.farm.animals.items():
            self.farm.animals[animal] = 999


class Exit(Option):
    def __init__(self, display_name):
        super().__init__(display_name)

    def execute(self):
        sys.exit()


class Turn:
    def __init__(self, option: Option):
        self.option = option

    def resolve_turn(self):
        self.option.execute()
