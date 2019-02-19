import unittest
from main import Breeder


class BreederTest(unittest.TestCase):
    def test_animal_breeding(self):
        self.assertEqual(Breeder.count_new_animals(2, 1), 1)
        self.assertEqual(Breeder.count_new_animals(3, 1), 2)
        self.assertEqual(Breeder.count_new_animals(0, 2), 1)
