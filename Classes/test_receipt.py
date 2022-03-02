from Shopping import ShoppingCart, Receipt
from dataclasses import MenuItem, Reservation
import unittest

class TestReceipt(unittest.TestCase):
    def setUp(self):
        '''Test some correctly initialized receipts'''
        #Receipt(List of Items, Reservation Object, Name)
        self.item1 = MenuItem("Macaroons", 6.00)
        self.item2 = MenuItem("New York Cheesecakes", 12.00)
        self.item3 = MenuItem("Banana Bread", 3.00)    
        self.item4 = MenuItem("Capuccino", 3.00)
        self.item5 = MenuItem("BLT", 10.00)
        self.item6 = MenuItem("French Croissant", 5.00)

        self.reservation1 = Reservation("Sunday", "9:00", "AM")
        self.reservation2 = Reservation("Tuesday", "5:00", "pm")

        self.receipt1 = Receipt([self.item1, self.item2, self.item3], self.reservation1, "Yariel")
        self.receipt2 = Receipt([self.item4, self.item5, self.item6, self.item3], None, "Xavier")

    def test_init(self):
        'Testing Items field'
        self.assertRaises(TypeError, Receipt, False, self.reservation1, "Bob")
        self.assertRaises(TypeError, Receipt, None, self.reservation1, "Bob")
        self.assertRaises(TypeError, Receipt, 10.38, self.reservation1, "Bob")
        self.assertRaises(TypeError, Receipt, "2x Cake", self.reservation1, "Bob")
        self.assertRaises(TypeError, Receipt, {}, self.reservation1, "Bob") 
        self.assertRaises(TypeError, Receipt, MenuItem("Macaroons", 7.00, 1), self.reservation1, "Bob")
        self.assertRaises(ValueError, Receipt, [], self.reservation1, "Bob") #Can't make a reservation without food
        self.assertRaises(ValueError, Receipt, ["Banana", "Coconut"], self.reservation1, "Bob") 
        self.assertRaises(ValueError, Receipt, [15, 13], self.reservation1, "Bob") 
        'Testing Reservations field'
        self.assertRaises(TypeError, Receipt, [self.item4], True, "Bob")
        self.assertRaises(TypeError, Receipt, [self.item4], 5.00, "Bob")
        self.assertRaises(TypeError, Receipt, [self.item4], (1+2j), "Bob")
        self.assertRaises(TypeError, Receipt, [self.item4], {}, "Bob")
        'Testing Names Field'
        self.assertRaises(TypeError, Receipt, [self.item4], self.reservation2, 1010)
        self.assertRaises(TypeError, Receipt, [self.item4], self.reservation2, None)
        self.assertRaises(TypeError, Receipt, [self.item4], self.reservation2, ['J', 'o', 'h', 'n'])
        self.assertRaises(TypeError, Receipt, [self.item4], self.reservation2, (5+10j))
        self.assertRaises(TypeError, Receipt, [self.item4], self.reservation2, 323.100)
        self.assertRaises(TypeError, Receipt, [self.item4], None, {})
        self.assertRaises(ValueError, Receipt, [self.item4], None, "") 
        self.assertRaises(ValueError, Receipt, [self.item4], None, "  ") #No empty names 
        self.assertRaises(ValueError, Receipt, [self.item4], None, "34Ronald87") 
        self.assertRaises(ValueError, Receipt, [self.item4], None, "Candace@White") #No Numeric names

    def test_values(self):
        '''Tests the Receipt class along with its methods.'''
        self.assertAlmostEquals(self.receipt1.subtotal(), 45.00)
        self.assertAlmostEquals(self.receipt2.subtotal(), 21.00)
        self.assertAlmostEquals(self.receipt1.tax(), 3.15)
        self.assertAlmostEquals(self.receipt2.tax(), 1.47)
        self.assertAlmostEquals(self.receipt1.total(), 48.15)
        self.assertAlmostEquals(self.receipt2.total(), 22.47)
        #[Menu Items], Subtotal, Tax, Total, Reservation, Name] -> will get passed to string format for the CLI to generate the receipt
        self.assertCountEqual(self.receipt1.get_order(), [[self.item1, self.item2, self.item3], 45.00, 3.15, 48.15,  self.reservation1, "Yariel"])
        self.assertCountEqual(self.receipt2.get_order(), [[self.item4, self.item5, self.item6, self.item3], 21.00, 1.47, 22.47, None, "Xavier"])


if __name__ == "__main__":
    unittest.main(failfast=True)
