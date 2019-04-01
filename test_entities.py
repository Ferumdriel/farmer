import unittest
from entities import AnimalType, Breeder, Dice, Farm


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

        _check_farm(animals={AnimalType.RABBIT: 2, AnimalType.SHEEP: 0, AnimalType.PIG: 2},
                    dice_animals=[AnimalType.RABBIT, AnimalType.SHEEP, AnimalType.SHEEP],
                    expected_total_animals={AnimalType.RABBIT: 3, AnimalType.SHEEP: 1, AnimalType.PIG: 2})
        _check_farm(animals={AnimalType.RABBIT: 2, AnimalType.SHEEP: 0, AnimalType.PIG: 2},
                    dice_animals=[AnimalType.RABBIT, AnimalType.WOLF, AnimalType.SHEEP],
                    expected_total_animals={AnimalType.RABBIT: 0, AnimalType.SHEEP: 0, AnimalType.PIG: 0})
        _check_farm(animals={AnimalType.RABBIT: 2, AnimalType.SHEEP: 0, AnimalType.PIG: 2},
                    dice_animals=[AnimalType.FOX, AnimalType.RABBIT, AnimalType.RABBIT],
                    expected_total_animals={AnimalType.RABBIT: 0, AnimalType.SHEEP: 0, AnimalType.PIG: 2})


class DiceTest(unittest.TestCase):
    def test_throw(self):
        def _check_dice(animals, checked_idx, expected_return):
            dice = Dice(animals)
            self.assertEqual(dice._get_side_animal_by_idx(checked_idx), expected_return)

        _check_dice([AnimalType.RABBIT, AnimalType.SHEEP], 0, AnimalType.RABBIT)
        _check_dice([], 0, None)
        _check_dice([AnimalType.RABBIT, AnimalType.SHEEP], 2, None)
