from statics import MenuItem, Reservation
import unittest

class TestMenuItem(unittest.TestCase):
    '''Tests the MenuItem dataclass along with its methods.'''
    def setUp(self):
        try:
            self.item1 = MenuItem(
                "Espresso",
                3,
                "https://bit.ly/3Ljp8xC",
                "The staple drink of italian origin, the espresso offers a strong coffee taste, showing the bean's flavor as well as leaving a nice crema on top to enjoy."
            )
        except:
            print("Failed to set up test menu test values!")

    def test_types(self):
        self.assertRaises(TypeError, MenuItem, None, 5.00, "some_link", "some_description", 1)
        self.assertRaises(TypeError, MenuItem, "item_name", None, "some_link", "some_description", 1)
        self.assertRaises(TypeError, MenuItem, "item_name", 1, ["some_link"], "ds", 1)
        self.assertRaises(TypeError, MenuItem, "some_name", 10, "link", 40, 1)

    def test_values(self):
        self.assertRaises(ValueError, MenuItem, "", 10, "link", "description")
        self.assertRaises(ValueError, MenuItem, "item_name", -2, "link", "description")
        self.assertRaises(ValueError, MenuItem, "item_name", 5.00, "", "description", 1)
        self.assertRaises(ValueError, MenuItem, "item_name", 6.00, "link", "", 1)
        self.assertRaises(ValueError, MenuItem, "Macaroons", 6.00, "https://bit.ly/3M6jfEi", "Almond dessert", -11) 
        'Optional parameter testing'
        self.assertraises(ValueError, MenuItem, "Banana Bread", 2, "A delicious sweet bread") #price not included. Only name, count, and desc
        self.assertraises(ValueError, MenuItem, "Banana Bread", 2.00, "link_here") #amount not included. Only name, price, and img link
        'Item not on the menu'
        self.assertRaises(ValueError, MenuItem, "Creme Brulee", 6.00, 1) 
        self.assertRaises(ValueError, MenuItem, "Hamburger", 6.00, "https://bit.ly/3M6jfEi", "Borger", 1) 

class TestReservation(unittest.TestCase):
    def test_init(self):
        'Testing days'
        self.assertRaises(TypeError, Reservation, None, "9:30", "am")
        self.assertRaises(TypeError, Reservation, 35, "9:30", "am")
        self.assertRaises(TypeError, Reservation, ["Sunday"], "9:30", "am")
        self.assertRaises(ValueError, Reservation, "Marcredi", "9:30", "am") #not a valid working day
        'Testing time'
        self.assertRaises(TypeError, Reservation, "Sunday", 930, "am")
        self.assertRaises(TypeError, Reservation, "Sunday", 1200, "am")
        self.assertRaises(TypeError, Reservation, "Sunday", [9, 0], "am")
        self.assertRaises(ValueError, Reservation, "Sunday", "13:00", "am")
        self.assertRaises(ValueError, Reservation, "Sunday", "900", "am")
        self.assertRaises(ValueError, Reservation, "Sunday", "0:50", "am")
        self.assertRaises(ValueError, Reservation, "Sunday", "12 : 50", "am")
        self.assertRaises(ValueError, Reservation, "Sunday", "1:30 PM", "am")
        'Test meridiem'
        self.assertRaises(TypeError, Reservation, "Tuesday", "4:00", 1)
        self.assertRaises(TypeError, Reservation, "Tuesday", "4:00", ['a', 'm'])
        self.assertRaises(TypeError, Reservation, "Tuesday", "4:00", None)
        self.assertRaises(ValueError, Reservation, "Tuesday", "4:00", 'am pm')
        self.assertRaises(ValueError, Reservation, "Tuesday", "4:00", 'a m')
        self.assertRaises(ValueError, Reservation, "Tuesday", "4:00", 'p m')
        self.assertRaises(ValueError, Reservation, "Tuesday", "4:00", 'ap')
        'Not under working hours'
        self.assertRaises(ValueError, Reservation, "Sunday", "3:01", "PM")
        self.assertRaises(ValueError, Reservation, "Wednesday", "6:59", "AM")
        self.assertRaises(ValueError, Reservation, "Friday", "6:00", "PM")

if __name__ == "__main__":
    unittest.main(failfast=True)
