import unittest
from main import Breeder


class BreederTest(unittest.TestCase):
    def test_new_animals_counting(self):
        self.assertEqual(Breeder.count_new_animals(2, 1), 1)
        self.assertEqual(Breeder.count_new_animals(3, 1), 2)
        self.assertEqual(Breeder.count_new_animals(0, 2), 1)
        self.assertEqual(Breeder.count_new_animals(3, 0), 0)


class FarmTest(unittest.TestCase):
    def test_animals_breeding(self):
        farm = Farm()
        existing_animals = [2, 0, 2]
        dice_animals = [1, 2, 0]
        new_animals = [Breeder.count_new_animals(ex, dice) for ex, dice in zip(existing_animals, dice_animals)]
        expected_total_animals = [3, 1, 2]
        counted_total_animals = farm.breed_animals(dice_animals)
        self.assertEquals(expected_total_animals, self.total_animals)