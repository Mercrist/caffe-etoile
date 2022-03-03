from collections import namedtuple
from statics import MenuItem

menu = {
    #coffee
    "espresso": MenuItem("Espresso", 1.00, "Coffee"), 
    "cappuccino": MenuItem("Cappuccino", 3.00, "Coffee"), 
    "americano": MenuItem("Americano", 2.00, "Coffee"),
    "vietnamese egg coffee": MenuItem("Vietnamese Egg Coffee", 3.00, "Specialty"),
    "cuban cortadito": MenuItem("Cuban Cortadito", 3.00, "Specialty"),
    "turkish coffee": MenuItem("Turkish Coffee", 3.00, "Specialty"), 

    #sandwiches
    "breakfast panini": MenuItem("Breakfast Panini", 7.00, "Sandwiches"),
    "avocado toast": MenuItem("Avocado Toast", 5.00, "Sandwiches"),
    "blt": MenuItem("BLT", 5.00, "Sandwiches"),

    #pastries
    "french croissant": MenuItem("French Croissant", 3.00, "Pastries"),
    "puerto rican quesito": MenuItem("Puerto Rican Quesito", 2.00, "Pastries"),
    "mexican concha" : MenuItem("Mexican Concha", 3.00, "Pastries"), 

    #desserts
    "banana bread": MenuItem("Banana Bread", 3.00, "Desserts"), 
    "new york cheesecake": MenuItem("New York Cheesecake", 4.00, "Desserts"),
    "macaroons": MenuItem("Macaroons", 2.00, "Desserts")
    }

hour_format = namedtuple('hour_format', 'hour, meridiem') #accessing the opened and closing hours by .get(day)[0 or 1].hour and .meridiem

working_hours = {
    "sunday": [hour_format("9:00", "AM"), hour_format("3:00", "PM")],
    "monday": [hour_format("7:00", "AM"), hour_format("5:00", "PM")],
    "tuesday": [hour_format("7:00", "AM"), hour_format("5:00", "PM")],
    "wednesday": [hour_format("7:00", "AM"), hour_format("5:00", "PM")],
    "thursday": [hour_format("7:00", "AM"), hour_format("5:00", "PM")],
    "friday": [hour_format("7:00", "AM"), hour_format("3:00", "PM")],
    "saturday": [hour_format("9:00", "AM"), hour_format("3:00", "PM")]
}