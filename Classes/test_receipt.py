from statics import MenuItem, Reservation
from Shopping import Receipt
import unittest

class TestReceipt(unittest.TestCase):
    def setUp(self):
        '''Test some correctly initialized receipts'''
        #Receipt(Dictionary of Items, Reservation Object, Name)
        self.reservation1 = Reservation("Sunday", "9:00", "AM")
        self.reservation2 = Reservation("Tuesday", "5:00", "pm")

        self.receipt1 = Receipt({"Macaroons": 1, "New York Cheesecakes": 2, "Banana Bread": 2}, self.reservation1, "Yariel")
        self.receipt2 = Receipt({"Capuccino": 1, "BLT": 2, "French Croissant": 2, "Banana Bread": 1}, None, "Xavier")

    def test_init(self):
        'Testing Items field'
        self.assertRaises(TypeError, Receipt, False, self.reservation1, "Bob")
        self.assertRaises(TypeError, Receipt, None, self.reservation1, "Bob")
        self.assertRaises(TypeError, Receipt, 10.38, self.reservation1, "Bob")
        self.assertRaises(TypeError, Receipt, "2x Cake", self.reservation1, "Bob")
        self.assertRaises(TypeError, Receipt, [], self.reservation1, "Bob") 
        self.assertRaises(TypeError, Receipt, MenuItem("Macaroons", 7.00), self.reservation1, "Bob")
        self.assertRaises(TypeError, Receipt, ["Banana", "Coconut"], self.reservation1, "Bob") 
        self.assertRaises(TypeError, Receipt, [15, 13], self.reservation1, "Bob") 
        self.assertRaises(ValueError, Receipt, {}, self.reservation1, "Bob") #Can't make a reservation without food
        self.assertRaises(ValueError, Receipt, {"Macaroons": 0}, self.reservation1, "Bob") #Need an amount
        self.assertRaises(ValueError, Receipt, {"Macaroons": None}, self.reservation1, "Bob")
        self.assertRaises(ValueError, Receipt, {"Macaroons": -1}, self.reservation1, "Bob") 
        'Testing Reservations field'
        self.assertRaises(TypeError, Receipt, {"Espresso": 1}, True, "Bob")
        self.assertRaises(TypeError, Receipt, {"Espresso": 1}, [], "Bob")
        self.assertRaises(TypeError, Receipt, {"Espresso": 1}, 5.00, "Bob")
        self.assertRaises(TypeError, Receipt, {"Espresso": 1}, (1+2j), "Bob")
        self.assertRaises(TypeError, Receipt, {"Espresso": 1}, {}, "Bob")
        self.assertRaises(TypeError, Receipt, {"Espresso": 1}, "Sunday", "Bob")
        self.assertRaises(TypeError, Receipt, {"Espresso": 1}, "9:00", "Bob")
        'Testing Names Field'
        self.assertRaises(TypeError, Receipt, {"Espresso": 1}, self.reservation2, 1010)
        self.assertRaises(TypeError, Receipt, {"Espresso": 1}, self.reservation2, None)
        self.assertRaises(TypeError, Receipt, {"Espresso": 1}, self.reservation2, ['J', 'o', 'h', 'n'])
        self.assertRaises(TypeError, Receipt, {"Espresso": 1}, self.reservation2, (5+10j))
        self.assertRaises(TypeError, Receipt, {"Espresso": 1}, self.reservation2, 323.100)
        self.assertRaises(TypeError, Receipt, {"Espresso": 1}, None, {})
        self.assertRaises(ValueError, Receipt, {"Espresso": 1}, None, "") 
        self.assertRaises(ValueError, Receipt, {"Espresso": 1}, None, "  ") #No empty names 
        self.assertRaises(ValueError, Receipt, {"Espresso": 1}, None, "34Ronald87") 
        self.assertRaises(ValueError, Receipt, {"Espresso": 1}, None, "Candace@White") #No Numeric names

    def test_values(self):
        '''Tests the Receipt class along with its methods.'''
        self.assertAlmostEquals(self.receipt1.subtotal(), 36.00)
        self.assertAlmostEquals(self.receipt2.subtotal(), 26.00)
        self.assertAlmostEquals(self.receipt1.tax(), 2.52)
        self.assertAlmostEquals(self.receipt2.tax(), 1.82)
        self.assertAlmostEquals(self.receipt1.total(), 38.52)
        self.assertAlmostEquals(self.receipt2.total(), 27.82)
        #[Menu Items], Subtotal, Tax, Total, Reservation, Name] -> will get passed to string format for the CLI to generate the receipt
        self.assertCountEqual(self.receipt1.get_order(), [{"Macaroons": 1, "New York Cheesecakes": 2, "Banana Bread": 2}, 36.00, 2.52, 38.52,  self.reservation1, "Yariel"])
        self.assertCountEqual(self.receipt2.get_order(), [{"Capuccino": 1, "BLT": 2, "French Croissant": 2, "Banana Bread": 1}, 26.00, 1.82, 27.82, None, "Xavier"])


if __name__ == "__main__":
    unittest.main(failfast=True)
