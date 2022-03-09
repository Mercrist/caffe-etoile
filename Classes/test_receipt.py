from Statics import Reservation
from Shopping import Receipt
import unittest

class TestReceipt(unittest.TestCase):
    def setUp(self):
        '''Test some correctly initialized receipts'''
        #Receipt(Dictionary of Items, Reservation Object, Name, subtotal)
        self.reservation1 = Reservation("Sunday", "9:00", "AM")
        self.reservation2 = Reservation("Tuesday", "5:00", "pm")

        self.receipt1 = Receipt({"Macaroons": 1, "New York Cheesecakes": 2, "Banana Bread": 2}, self.reservation1, "Yariel", 36.00)
        self.receipt2 = Receipt({"Cappuccino": 1, "BLT": 2, "French Croissant": 2, "Banana Bread": 1}, self.reservation2, "Xavier", 26.00)

    def test_init(self):
        'Testing Items field'
        self.assertRaises(TypeError, Receipt, False, self.reservation1, "Bob",26.00)
        self.assertRaises(TypeError, Receipt, None, self.reservation1, "Bob",26.00)
        self.assertRaises(TypeError, Receipt, 10.38, self.reservation1, "Bob",26.00)
        self.assertRaises(TypeError, Receipt, "2x Cake", self.reservation1, "Bob",26.00)
        self.assertRaises(TypeError, Receipt, [], self.reservation1, "Bob",26.00) 
        self.assertRaises(TypeError, Receipt, ["Banana", "Coconut"], self.reservation1, "Bob",26.00) 
        self.assertRaises(TypeError, Receipt, [15, 13], self.reservation1, "Bob",26.00) 
        self.assertRaises(ValueError, Receipt, {"Macaroons": None}, self.reservation1, "Bob",26.00)
        self.assertRaises(ValueError, Receipt, {"Macaroons": -1}, self.reservation1, "Bob",26.00) 
        self.assertRaises(ValueError, Receipt, {}, self.reservation1, "Bob",26.00) #can't generate a receipt with no items
        'Testing Reservations field'
        self.assertRaises(TypeError, Receipt, {"Espresso": 1}, True, "Bob",26.00)
        self.assertRaises(TypeError, Receipt, {"Espresso": 1}, [], "Bob",26.00)
        self.assertRaises(TypeError, Receipt, {"Espresso": 1}, 5.00, "Bob",26.00)
        self.assertRaises(TypeError, Receipt, {"Espresso": 1}, (1+2j), "Bob",26.00)
        self.assertRaises(TypeError, Receipt, {"Espresso": 1}, {}, "Bob",26.00)
        self.assertRaises(TypeError, Receipt, {"Espresso": 1}, "Sunday", "Bob",26.00)
        self.assertRaises(TypeError, Receipt, {"Espresso": 1}, "9:00", "Bob",26.00)
        'Testing Names Field'
        self.assertRaises(TypeError, Receipt, {"Espresso": 1}, self.reservation2, 1010, 26.00)
        self.assertRaises(TypeError, Receipt, {"Espresso": 1}, self.reservation2, None, 26.00)
        self.assertRaises(TypeError, Receipt, {"Espresso": 1}, self.reservation2, ['J', 'o', 'h', 'n'], 26.00)
        self.assertRaises(TypeError, Receipt, {"Espresso": 1}, self.reservation2, (5+10j), 26.00)
        self.assertRaises(TypeError, Receipt, {"Espresso": 1}, self.reservation2, 323.100, 26.00)
        self.assertRaises(TypeError, Receipt, {"Espresso": 1}, self.reservation2, {}, 26.00)
        self.assertRaises(ValueError, Receipt, {"Espresso": 1}, self.reservation2, "", 26.00) 
        self.assertRaises(ValueError, Receipt, {"Espresso": 1}, self.reservation2, "  ", 26.00) #No empty names 
        self.assertRaises(ValueError, Receipt, {"Espresso": 1}, self.reservation2, "34Ronald87", 26.00) 
        self.assertRaises(ValueError, Receipt, {"Espresso": 1}, self.reservation2, "Candace@White",26.00) #No Numeric names
        'Testing subtotal'
        self.assertRaises(TypeError, Receipt, {"Espresso": 1}, self.reservation2, "Bob", True)
        self.assertRaises(TypeError, Receipt, {"Espresso": 1}, self.reservation2, "Bob", [10.25])
        self.assertRaises(TypeError, Receipt, {"Espresso": 1}, self.reservation2, "Bob", None)
        self.assertRaises(ValueError, Receipt, {"Espresso": 1}, self.reservation2, "Bob", -3.12)
        self.assertRaises(ValueError, Receipt, {"Espresso": 1}, self.reservation2, "Bob", 0)

    def test_values(self):
        '''Tests the Receipt class along with its methods.'''
        self.assertAlmostEqual(self.receipt1.subtotal, 36.00)
        self.assertAlmostEqual(self.receipt2.subtotal, 26.00)
        self.assertAlmostEqual(self.receipt1.tax(), 3.69)
        self.assertAlmostEqual(self.receipt2.tax(), 2.67)
        self.assertAlmostEqual(self.receipt1.total(), 39.69)
        self.assertAlmostEqual(self.receipt2.total(), 28.67)
        self.assertEqual(self.receipt1.receipt_number(), "2017396003")
        self.assertEqual(self.receipt2.receipt_number(), "2316286004")

if __name__ == "__main__":
    unittest.main(failfast=True)
