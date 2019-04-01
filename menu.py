from actions import DiceRoller, Trader, Cheatmode, Exit


class GameMenu:
    def __init__(self, game):
        self.game = game
        self.options = {1: DiceRoller('Roll dices', game.dices, game.farm),
                        2: Trader('Trade', game.farm),
                        3: Cheatmode('CHEATMODE', game.farm),
                        4: Exit('Exit')}

    def get_option(self, option_number):
        return self.options[option_number]

    def print_options(self):
        print('Which option do you choose?')
        print(self.options_txt)

    @property
    def options_txt(self):
        opt_text = ''
        for key, value in self.options.items():
            opt_text += f'{key}. {value}\n'
        return opt_text
