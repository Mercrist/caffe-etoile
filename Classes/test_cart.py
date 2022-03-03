from multiprocessing.sharedctypes import Value
import unittest 
from Shopping import ShoppingCart 
from statics import MenuItem, Reservation


class TestShoppingCart(unittest.TestCase):
    def setUp(self) -> None:
        self.cart = ShoppingCart("xavier")
        self.cart2 = ShoppingCart("yariel")
        self.cart2.add_items('Espresso',1)
        self.cart2.add_items('Americano',3)
        self.cart2.set_reservation('Sunday','12:00','PM')
    def test_types(self):
        self.assertRaises(TypeError,self.cart.add_items,10,5)
        self.assertRaises(TypeError, self.cart.add_items,"Espresso","1")
        self.assertRaises(TypeError, self.cart.add_items,"Espresso", 1.24)
        self.assertRaises(TypeError, self.cart.add_items, 10, 1)
        self.assertRaises(TypeError, self.cart.set_reservation,None) #TODO 
        self.assertRaises(TypeError, self.cart.set_reservation, "Sunday","9:00",10)
        self.assertRaises(TypeError, self.remove_items,1)
        self.assertRaises(TypeError, ShoppingCart, 10)
        self.assertRaises(TypeError, ShoppingCart, None)

    def test_values(self):
        self.assertRaises(ValueError, ShoppingCart, "")
        self.assertRaises(ValueError, ShoppingCart, " ")
        self.assertRaises(ValueError, ShoppingCart, "X3vier")
        self.assertRaises(ValueError, ShoppingCart, 'X@v1er')
        self.assertRaises(ValueError, ShoppingCart, "a")
        self.assertRaises(ValueError, self.cart.add_items,"Espresso",-1)
        self.assertRaises(ValueError, self.cart.add_items,"Not an item",1)
        self.assertRaises(ValueError, self.cart.add_items,"New York Cheesecake", 2)
        self.assertRaises(ValueError, self.cart.remove_items,"Item not in cart", 1)
        self.assertRaises(ValueError, self.cart.remove_items,"Espresso", 10) #remove more espressos than in cart
        self.assertRaises(ValueError, self.cart.set_reservation,"Saturday","1:00","AM")
        self.assertRaises(ValueError, self.cart.set_reservation,"Monday", "4:00", "AM")
        self.assertRaises(ValueError, self.cart.set_reservation,"twensday", "4:00","PM")
        self.assertRaises(ValueError, self.cart.set_reservation,"Monday","100:00", "AM")
        self.assertRaises(ValueError, self.cart.set_reservation, "Monday", "10:00", "MM")

    def test_cart_attributes(self):
        self.assertTrue(len(self.cart.items) == 0) 
        self.assertTrue(self.cart.total == 0.00)
        self.assertTrue(len(self.cart2.items) == 4)
        self.assertTrue(self.cart2.reservation == Reservation("Sunday","12:00","PM"))


