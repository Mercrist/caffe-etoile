from Shopping import ShoppingCart, Receipt
import unittest

class TestReceipt(unittest.TestCase, Receipt):
    '''Tests the Receipt class along with its methods.'''
    def test_values(self):
        self.assertAlmostEquals(subtotal(), 21.00)
        self.assertAlmostEquals(subtotal(), 19.26)
        self.assertAlmostEquals(tax(21.00), 1.47)
        self.assertAlmostEquals(tax(18.00), 1.26)
        #[{Item: [Freq, Price]}, Subtotal, Tax, Total, Name] -> will get passed to string format for the CLI to generate the receipt
        self.assertCountEqual(get_order(), [{"Macaroons": [3, 6.00], "New York Cheesecakes": [2, 12.00], "Banana Bread": [1, 3.00]}, 21.00, 1.47, 22.47, "Yariel"])
        self.assertCountEqual(get_order(), [{"Capuccino": [1, 3.00], "BLT": [1, 10.00], "French Croissant": [1, 5.00]}, 18.00, 1.26, 19.26, "Xavier"])

    def test_types(self):
        'Test for value errors'
        self.assertRaises(ValueError, tax, 100)
        self.assertRaises(ValueError, tax, 200)
        self.assertRaises(ValueError, tax, -3.60)
        self.assertRaises(ValueError, tax, 0.00)
        'Test for type errors'
        self.assertRaises(TypeError, self._order, [])
        self.assertRaises(TypeError, self._order, True)
        self.assertRaises(TypeError, self._order, None)
        self.assertRaises(TypeError, self._order, (1+5j))
        self.assertRaises(TypeError, self._order, 7.5)
        self.assertRaises(TypeError, self._order, "cost")
        self.assertRaises(TypeError, self._time, 5)
        self.assertRaises(TypeError, self._time, [])
        self.assertRaises(TypeError, self._time, True)
        self.assertRaises(TypeError, self._time, -7.8)
        self.assertRaises(TypeError, self._time, (1+5j))
        self.assertRaises(TypeError, self._time, [])
        self.assertRaises(TypeError, self._time, {})
        self.assertRaises(TypeError, self._name, 5)
        self.assertRaises(TypeError, self._name, [])
        self.assertRaises(TypeError, self._name, True)
        self.assertRaises(TypeError, self._name, -7.8)
        self.assertRaises(TypeError, self._name, (1+5j))
        self.assertRaises(TypeError, self._name, [])
        self.assertRaises(TypeError, self._name, {})
        self.assertRaises(TypeError, tax, {})
        self.assertRaises(TypeError, tax, True)
        self.assertRaises(TypeError, tax, None)
        self.assertRaises(TypeError, tax, (1+10j))
        self.assertRaises(TypeError, tax, "7%")


class TestCart(unittest.TestCase):
    '''Tests the Receipt class along with its methods.'''
    def test_types(self):
        pass

    def test_values(self):
        pass


if __name__ == "__main__":
    unittest.main()
