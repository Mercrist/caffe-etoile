from items import MenuItem
import unittest

class TestMenuItem(unittest.TestCase):
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
    '''Tests the MenuItem dataclass along with its methods.'''
    def test_types(self):
        self.assertRaises(TypeError, MenuItem, None, 5, "some_link", "some_description")
        self.assertRaises(TypeError, MenuItem, "item_name", None, "some_link", "some_description")
        self.assertRaises(TypeError, MenuItem, "item_name", 1, ["some_link"], "ds")
        self.assertRaises(TypeError, MenuItem, "some_name", 10, "link", 40)
    def test_values(self):
        self.assertRaises(ValueError, MenuItem, "", 10, "link", "description")
        self.assertRaises(ValueError, MenuItem, "item_name", -2, "link", "description")
        self.assertRaises(ValueError, MenuItem, "item_name", 5, "", "description")
        self.assertRaises(ValueError, MenuItem, "item_name", 6, "link", "")


if __name__ == "__main__":
    unittest.main()
