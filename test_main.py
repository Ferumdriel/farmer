import unittest
from main import Breeder, Farm, Dice, Animal, Trade, TradeRule


class BreederTest(unittest.TestCase):
    def test_new_animals_counting(self):
        self.assertEqual(Breeder.count_new_animals(2, 1), 1)
        self.assertEqual(Breeder.count_new_animals(3, 1), 2)
        self.assertEqual(Breeder.count_new_animals(0, 2), 1)
        self.assertEqual(Breeder.count_new_animals(3, 0), 0)


class FarmTest(unittest.TestCase):
    def test_animals_breeding(self):
        def _check_farm(animals, dice_animals, expected_total_animals):
            farm = Farm(animals)
            dice_animals = dice_animals
            expected_total_animals = expected_total_animals
            farm.breed_animals(dice_animals)
            self.assertEqual(expected_total_animals, farm.animals)

        _check_farm(animals={Animal.RABBIT: 2, Animal.SHEEP: 0, Animal.PIG: 2},
                    dice_animals=[Animal.RABBIT, Animal.SHEEP, Animal.SHEEP],
                    expected_total_animals={Animal.RABBIT: 3, Animal.SHEEP: 1, Animal.PIG:2})
        _check_farm(animals={Animal.RABBIT: 2, Animal.SHEEP: 0, Animal.PIG: 2},
                    dice_animals=[Animal.RABBIT, Animal.WOLF, Animal.SHEEP],
                    expected_total_animals={Animal.RABBIT: 0, Animal.SHEEP: 0, Animal.PIG: 0})
        _check_farm(animals={Animal.RABBIT: 2, Animal.SHEEP: 0, Animal.PIG: 2},
                    dice_animals=[Animal.FOX, Animal.RABBIT, Animal.RABBIT],
                    expected_total_animals={Animal.RABBIT: 0, Animal.SHEEP: 0, Animal.PIG: 2})


class DiceTest(unittest.TestCase):
    def test_throw(self):
        def _check_dice(animals, checked_idx, expected_return):
            dice = Dice(animals)
            self.assertEqual(dice._get_side_animal_by_idx(checked_idx), expected_return)

        _check_dice([Animal.RABBIT, Animal.SHEEP], 0, Animal.RABBIT)
        _check_dice([], 0, None)
        _check_dice([Animal.RABBIT, Animal.SHEEP], 2, None)


class TradeTest(unittest.TestCase):
    def test_trade_conditions(self):
        trade_rule = TradeRule(Animal.RABBIT, Animal.SHEEP, 6)
        trade = Trade([trade_rule])
        self.assertTrue(trade.is_trade_possible(Animal.RABBIT, Animal.SHEEP, 12, 2))
        self.assertFalse(trade.is_trade_possible(Animal.RABBIT, Animal.SHEEP, 17, 3))
        self.assertFalse(trade.is_trade_possible(Animal.SHEEP, Animal.SHEEP, 1, 1))
        self.assertTrue(trade.is_trade_possible(Animal.SHEEP, Animal.RABBIT, 3, 15))
        self.assertTrue(trade.is_trade_possible(Animal.SHEEP, Animal.RABBIT, 3, 18))
