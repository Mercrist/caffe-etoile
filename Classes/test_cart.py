import unittest 
from Shopping import ShoppingCart 
from statics import MenuItem, Reservation

class TestShoppingCart(unittest.TestCase):
    def setUp(self):
        self.cart = ShoppingCart("xavier")
        self.cart2 = ShoppingCart("yariel")
        self.cart2.add_items('Espresso')
        self.cart2.add_items('Americano',3)
        self.cart2.add_items('Americano',7)
        self.cart2.add_items('new york cheesecake',7)
        self.cart2.set_reservation(Reservation('Sunday','12:00','PM'))

    def test_types(self):
        self.assertRaises(TypeError,self.cart.add_items(10,5))
        self.assertRaises(TypeError, self.cart.add_items("Espresso","1"))
        self.assertRaises(TypeError, self.cart.set_reservation()) #TODO 
        self.assertRaises(TypeError, self.remove_items(1))
        self.assertRaises(TypeError, ShoppingCart, 10)

    def test_values(self):
        self.assertRaises(ValueError, ShoppingCart, " ") #can't be empty
        self.assertRaises(ValueError, ShoppingCart, " ") #can't be empty
        self.assertRaises(ValueError, self.cart.add_items("Espresso",-1))
        self.assertRaises(ValueError, self.cart.add_items("Not an item",1))
        self.assertRaises(ValueError, self.cart.add_items("new York cheesecake", 2))
        self.assertRaises(ValueError, self.cart.add_items("americano", 2)) # theres already 10 americanos, the max amount of items you can have
        self.assertRaises(ValueError, self.cart.remove_items("Item not in cart", 1))
        self.assertRaises(ValueError, self.cart.remove_items("Espresso", 10)) #remove more espressos than in cart
        self.assertRaises(ValueError, self.cart.remove_items("new york cheesecake", 8)) #remove more espressos than in cart
        self.assertRaises(ValueError, self.cart.set_reservation("Saturday","1:00","AM"))
        self.assertRaises(ValueError, self.cart.set_reservation("Monday", "4:00", "AM"))
        self.assertRaises(ValueError, self.cart.set_reservation("twensday", "4:00","PM"))
        self.assertRaises(ValueError, self.cart.set_reservation("Monday","100:00", "AM"))
        self.assertRaises(ValueError, self.cart.set_reservation("Monday","100:00", "AM"))


    def test_cart_attributes(self):
        self.assertTrue(len(self.cart.items) == 0) 
        self.assertTrue(self.cart.reservation == None)
        self.assertTrue(self.cart.total == 0.00)
        self.assertTrue(len(self.cart2.items) == 4)
        self.assertTrue(self.cart2.reservation == Reservation("Sunday","12:00","PM"))

