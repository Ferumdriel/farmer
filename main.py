from menu import GameMenu
from entities import AnimalType, Dice, Farm
from utils import InputListener
from actions import Turn


class Game:
    def __init__(self):
        self.farm = Farm()
        self.dices = [
            Dice(6 * [AnimalType.RABBIT] + 3 * [AnimalType.SHEEP] + [AnimalType.PIG, AnimalType.COW, AnimalType.WOLF]),
            Dice(6 * [AnimalType.RABBIT] + 2 * [AnimalType.SHEEP, AnimalType.PIG] + [AnimalType.HORSE, AnimalType.FOX])]
        self.menu = GameMenu(self)
        self.turns = []

    def resolve_turn(self):
        self.menu.print_options()
        picked_option = InputListener.get_int_input()
        option = self.menu.get_option(picked_option)
        turn = Turn(option)
        turn.resolve_turn()
        self.turns.append(turn)

    def main_loop(self):
        while True:
            self.resolve_turn()


if __name__ == '__main__':
    game = Game()
    game.main_loop()
