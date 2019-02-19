import unittest

class BreederTest(unittest.TestCase):
    def test_animal_breeding(self):
        current_animals = 2
        dice_animals = 1
        result = Breeder.count_new_animals(current_animals, dice_animals)
        self.assertEqual(result, 1)