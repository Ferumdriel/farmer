from abc import abstractmethod, ABC


class Option(ABC):
    @abstractmethod
    def execute(self):
        pass


class DiceRoller(Option):
    def __init__(self, dices, farm):
        self.dices = dices
        self.farm = farm

    def execute(self):
        animals = [dice.throw() for dice in self.dices]
        print(f'You threw: {animals}')
        self.farm.breed_animals(animals)
        self.farm.print_state()

class Trader(Option):
    pass
class GameMenu:
    def __init__(self, game):
        self.options = {1: 'Roll dices',
                        2: 'Trade',
                        3: 'CHEATMODE',
                        4: 'Exit'}
        self.game = game
