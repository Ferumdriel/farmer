import unittest
from actions import TradeRequest
from entities import Farm, AnimalType


class TradeTest(unittest.TestCase):
    def test_trade_conditions(self):
        def case(sold_animal, bought_animal, available_amount, desired_amount, expected_result: bool):
            farm = Farm({sold_animal: available_amount, bought_animal: 0})
            func = self.assertTrue if expected_result else self.assertFalse
            func(TradeRequest(sold_animal, bought_animal, farm, desired_amount).is_trade_possible())

        case(AnimalType.RABBIT, AnimalType.SHEEP, 12, 2, True)
        case(AnimalType.RABBIT, AnimalType.SHEEP, 17, 3, False)
        case(AnimalType.SHEEP, AnimalType.SHEEP, 1, 1, False)
        case(AnimalType.SHEEP, AnimalType.RABBIT, 3, 15, True)
        case(AnimalType.SHEEP, AnimalType.RABBIT, 3, 18, True)

    def test_trade(self):
        farm = Farm({AnimalType.RABBIT: 30, AnimalType.SHEEP: 0, AnimalType.PIG: 2})
        trade = TradeRequest(AnimalType.RABBIT, AnimalType.SHEEP, farm, 3)
        expected_after_sell = farm.animals[AnimalType.RABBIT] - AnimalType.SHEEP.get_value() * 3
        expected_after_buy = farm.animals[AnimalType.SHEEP] + AnimalType.RABBIT.get_value() * 3
        trade.trade()
        self.assertEqual(farm.animals[AnimalType.RABBIT], expected_after_sell)
        self.assertEqual(farm.animals[AnimalType.SHEEP], expected_after_buy)