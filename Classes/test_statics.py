from statics import MenuItem, Reservation
import unittest

class TestMenuItem(unittest.TestCase):
    '''Tests the MenuItem dataclass along with its methods.'''
    def setUp(self):
        try:
            self.item1 = MenuItem("Espresso", 1.00, "Coffee",
            "The staple drink of italian origin, the espresso shot offers a strong coffee taste, \
            showing the bean's flavors as well as leaving a nice crema on the top to enjoy.",
            "https://bit.ly/3Ljp8xC")

        except:
            print("Failed to set up test menu test values!")

    def test_types(self):
        self.assertRaises(TypeError, MenuItem, None, 5.00, "some_category", "some_description", "some_link")
        self.assertRaises(TypeError, MenuItem, "item_name", None, "some_category", "some_description", "some_link")
        self.assertRaises(TypeError, MenuItem, "item_name", 2.00, {"____"}, "ds", "some_link")
        self.assertRaises(TypeError, MenuItem, "item_name", 2.00, "some_category", ["ds"], "some_link")
        self.assertRaises(TypeError, MenuItem, "item_name", 2.00, "some_category", "ds", ["some_link"])

    def test_values(self):
        'No valid food name'
        self.assertRaises(ValueError, MenuItem, "    ", 10, "Desserts", "description", "https://bit.ly/3INsUxy") #No empty names
        'No valid pricing'
        self.assertRaises(ValueError, MenuItem, "item_name", -2, "Desserts", "description", "link")
        self.assertRaises(ValueError, MenuItem, "item_name", 200, "Desserts", "description", "link") #excessive pricing
        self.assertRaises(ValueError, MenuItem, "item_name", 80, "Desserts", "description", "link") 
        'No valid descriptions'
        self.assertRaises(ValueError, MenuItem, "item_name", 5.00, "Desserts", "     ", "link") 
        self.assertRaises(ValueError, MenuItem, "item_name", 5.00, "Desserts", "", "link") 
        'Not valid categories'
        self.assertRaises(ValueError, MenuItem, "Macaroons", 6.00, "Almond dessert", "desc", "https://bit.ly/3M6jfEi") #not a valid category 
        self.assertRaises(ValueError, MenuItem, "Macaroons", 6.00, "Entree", "desc", "https://bit.ly/3M6jfEi")  
        self.assertRaises(ValueError, MenuItem, "Macaroons", 6.00, "Pasta", "desc", "https://bit.ly/3M6jfEi") 
        'No valid urls'
        self.assertRaises(ValueError, MenuItem, "Macaroons", 6.00, "Desserts", "desc", "") 
        self.assertRaises(ValueError, MenuItem, "Macaroons", 6.00, "Desserts", "desc", " ") 


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
        self.assertRaises(ValueError, Reservation, "Thursday", "6:58", "AM")

if __name__ == "__main__":
    unittest.main(failfast=True)
