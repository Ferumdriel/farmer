from abc import ABC, abstractmethod
from main import Dice


class ActionCommand(ABC):
    # def __init__(self, action, previous_action=None):
    #     self.action = action
    #     self.previous_action = previous_action
    @abstractmethod
    def execute(self):
        pass


class RollDiceCommand(ActionCommand):
    def __init__(self, dices: list):
        self.dices = dices

    def execute(self):
        for dice in self.dices:
            dice.result = dice.throw()

class TradeCommand(ActionCommand):
    def __init__(self, trade_request):
        self.trade_request = trade_request
    def execute(self):
        pass