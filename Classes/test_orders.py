from Shopping import ShoppingCart, Receipt
import unittest

class TestReceipt(unittest.TestCase):
    def setUp(self):
        #Receipt(Items, Time, Name)
        self.receipt1 = Receipt({"Macaroons": [3, 6.00], "New York Cheesecakes": [2, 12.00], "Banana Bread": [1, 3.00]}, ["Sunday", "9:00", "AM"], "Yariel")
        self.receipt2 = Receipt({"Capuccino": [1, 3.00], "BLT": [1, 10.00], "French Croissant": [1, 5.00], "Banana Bread": [1, 3.00]}, [], "Xavier")

    def test_init_types(self):
        'Testing Items field'
        self.assertRaises(TypeError, Receipt, False, ["Tuesday", "8:00", "AM"], "Bob")
        self.assertRaises(TypeError, Receipt, None, ["Tuesday", "8:00", "AM"], "Bob")
        self.assertRaises(TypeError, Receipt, 10.38, ["Tuesday", "8:00", "AM"], "Bob")
        self.assertRaises(TypeError, Receipt, [], ["Tuesday", "8:00", "AM"], "Bob")
        self.assertRaises(TypeError, Receipt, "2x Cake", ["Tuesday", "8:00", "AM"], "Bob")
        self.assertRaises(TypeError, Receipt, None, ["Tuesday", "8:00", "AM"], "Bob") 
        self.assertRaises(ValueError, Receipt, {}, ["Tuesday", "8:00", "AM"], "Bob") #Can't make an empty reservation
        'Testing Time field'
        self.assertRaises(TypeError, Receipt, {"Espresso": [1, 1.00]}, True, "Bob")
        self.assertRaises(TypeError, Receipt, {"Espresso": [1, 1.00]}, 5.00, "Bob")
        self.assertRaises(TypeError, Receipt, {"Espresso": [1, 1.00]}, (1+2j), "Bob")
        self.assertRaises(TypeError, Receipt, {"Espresso": [1, 1.00]}, {}, "Bob")
        self.assertRaises(TypeError, Receipt, {"Espresso": [1, 1.00]}, None, "Bob")
        self.assertRaises(ValueError, Receipt, {"Espresso": [1, 1.00]}, ["Saturday", "7:00"], "Bob") #can't have only two attributes
        'Testing Names Field'
        self.assertRaises(TypeError, Receipt, {"Espresso": [1, 1.00]}, ["Tuesday", "8:00", "AM"], 1010)
        self.assertRaises(TypeError, Receipt, {"Espresso": [1, 1.00]}, ["Tuesday", "8:00", "AM"], None)
        self.assertRaises(TypeError, Receipt, {"Espresso": [1, 1.00]}, ["Tuesday", "8:00", "AM"], ['J', 'o', 'h', 'n'])
        self.assertRaises(TypeError, Receipt, {"Espresso": [1, 1.00]}, ["Tuesday", "8:00", "AM"], (5+10j))
        self.assertRaises(TypeError, Receipt, {"Espresso": [1, 1.00]}, ["Tuesday", "8:00", "AM"], 323.100)
        self.assertRaises(TypeError, Receipt, {"Espresso": [1, 1.00]}, ["Tuesday", "8:00", "AM"], {})
        self.assertRaises(ValueError, Receipt, {"Espresso": [1, 1.00]}, ["Tuesday", "8:00", "AM"], "") #No empty names or numeric names
        self.assertRaises(ValueError, Receipt, {"Espresso": [1, 1.00]}, ["Tuesday", "8:00", "AM"], "  ")
        self.assertRaises(ValueError, Receipt, {"Espresso": [1, 1.00]}, ["Tuesday", "8:00", "AM"], "34Ronald87")

    def test_values(self):
        '''Tests the Receipt class along with its methods.'''
        self.assertAlmostEquals(self.receipt1.subtotal(), 45.00)
        self.assertAlmostEquals(self.receipt2.subtotal(), 21.00)
        self.assertAlmostEquals(self.receipt1.tax(), 3.15)
        self.assertAlmostEquals(self.receipt2.tax(), 1.47)
        self.assertAlmostEquals(self.receipt1.total(), 48.15)
        self.assertAlmostEquals(self.receipt2.total(), 22.47)
        #[{Item: [Freq, Price]}, Subtotal, Tax, Total, Time, Name] -> will get passed to string format for the CLI to generate the receipt
        self.assertCountEqual(self.receipt1.get_order(), [{"Macaroons": [3, 6.00], "New York Cheesecakes": [2, 12.00], "Banana Bread": [1, 3.00]}, 45.00, 3.15, 48.15, 
                              ["Sunday", "9:00", "AM"], "Yariel"])
        self.assertCountEqual(self.receipt2.get_order(), [{"Capuccino": [1, 3.00], "BLT": [1, 10.00], "French Croissant": [1, 5.00]}, 21.00, 1.47, 22.47, [], "Xavier"])


class TestCart(unittest.TestCase):
    '''Tests the Receipt class along with its methods.'''
    def test_types(self):
        pass

    def test_values(self):
        pass


if __name__ == "__main__":
    unittest.main(failfast=True)
