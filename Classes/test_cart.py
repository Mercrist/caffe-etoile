from Shopping import ShoppingCart 
from statics import Reservation
import unittest 

class TestShoppingCart(unittest.TestCase):
    def setUp(self):
        self.cart1 = ShoppingCart("xavier")
        self.cart1.set_reservation('Monday','12:00','PM')
        self.cart1.clear_reservation()
        self.cart2 = ShoppingCart("yariel")
        self.cart2.add_items('Espresso')
        self.cart2.add_items('Americano',3)
        self.cart2.add_items('Americano',7)
        self.cart2.add_items('new york cheesecake',7)
        self.cart2.set_reservation('Sunday','12:00','PM')

    def test_types(self):
        self.assertRaises(TypeError,self.cart.add_items,10,5)
        self.assertRaises(TypeError, self.cart.add_items,"Espresso","1")
        self.assertRaises(TypeError, self.cart.add_items,"Espresso", 1.24)
        self.assertRaises(TypeError, self.cart.add_items, 10, 1)
        self.assertRaises(TypeError, self.cart.remove_items, 1)
        self.assertRaises(TypeError, ShoppingCart, 10)
        self.assertRaises(TypeError, ShoppingCart, None)
        self.assertRaises(TypeError,self.cart1.add_items,10,5)
        self.assertRaises(TypeError, self.cart1.add_items,"Espresso","1")
        self.assertRaises(TypeError, self.cart1.add_items,"Espresso", 1.24)
        self.assertRaises(TypeError, self.cart1.add_items, 10, 1)
        self.assertRaises(TypeError, self.cart1.set_reservation, None, "12:30", "PM") 
        self.assertRaises(TypeError, self.cart1.set_reservation, "Sunday","9:00", 10)
        self.assertRaises(TypeError, self.cart1.remove_items, None, 30)

    def test_values(self):
        self.assertRaises(ValueError, ShoppingCart, "")
        self.assertRaises(ValueError, ShoppingCart, " ") #can't be empty
        self.assertRaises(ValueError, ShoppingCart, "X3vier")
        self.assertRaises(ValueError, ShoppingCart, 'X@v1er')
        self.assertRaises(ValueError, self.cart.add_items,"Espresso",-1)
        self.assertRaises(ValueError, self.cart.add_items,"Not an item",1)
        self.assertRaises(ValueError, self.cart.add_items,"New York Cheesecake", 4)
        self.assertRaises(ValueError, self.cart.add_items, "americano", 2) # theres already 10 americanos, the max amount of items you can have
        self.assertRaises(ValueError, self.cart.remove_items,"Item not in cart", 1)
        self.assertRaises(ValueError, self.cart.remove_items,"Espresso", 10) #remove more espressos than in cart
        self.assertRaises(ValueError, self.cart.remove_items,"Espresso", 20) #remove more espressos than in cart
        self.assertRaises(ValueError, self.cart.set_reservation,"Saturday","1:00","AM")
        self.assertRaises(ValueError, self.cart.set_reservation,"Monday", "4:00", "AM")
        self.assertRaises(ValueError, self.cart.set_reservation,"Sunday", "12:00", "AM")
        self.assertRaises(ValueError, self.cart.set_reservation,"twensday", "4:00","PM")
        self.assertRaises(ValueError, self.cart.set_reservation,"Monday","100:00", "AM")
        self.assertRaises(ValueError, self.cart.set_reservation, "Monday", "10:00", "MM")


    def test_cart_attributes(self):
        'Testing cart 1'
        self.assertEqual(len(self.cart1.cart), 0) 
        self.assertEqual(self.cart1.reservation, None)
        self.assertEqual(self.cart1.total_cost, 0.00)
        'Testing cart 2'
        self.assertEqual(len(self.cart2.cart), 3)
        self.assertEqual(self.cart2.reservation, Reservation("SuNdAy","12:00","PM"))
        self.assertEqual(self.cart2.total_cost, 49.00)

if __name__ == "__main__":
    unittest.main(failfast=True)