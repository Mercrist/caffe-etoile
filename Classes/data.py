from collections import namedtuple
from statics import MenuItem

menu = {
    #coffee
    "Espresso": MenuItem("Espresso", 1.00, "Coffee"), 
    "Cappuccino": MenuItem("Cappuccino", 3.00, "Coffee"), 
    "Americano": MenuItem("Americano", 2.00, "Coffee"),
    "Vietnamese Egg Coffee": MenuItem("Vietnamese Egg Coffee", 3.00, "Specialty"),
    "Cuban Cortadito": MenuItem("Cuban Cortadito", 3.00, "Specialty"),
    "Turkish Coffee": MenuItem("Turkish Coffee", 3.00, "Specialty"), 

    #sandwiches
    "Breakfast Panini": MenuItem("Breakfast Panini", 7.00, "Sandwiches"),
    "Avocado Toast": MenuItem("Avocado Toast", 5.00, "Sandwiches"),
    "BLT": MenuItem("BLT", 5.00, "Sandwiches"),

    #pastries
    "French Croissant": MenuItem("French Croissant", 3.00, "Pastries"),
    "Puerto Rican Quesito": MenuItem("Puerto Rican Quesito", 2.00, "Pastries"),
    "Mexican Concha" : MenuItem("Mexican Concha", 3.00, "Pastries"), 

    #desserts
    "Banana Bread": MenuItem("Banana Bread", 3.00, "Desserts"), 
    "New York Cheesecake": MenuItem("New York Cheesecake", 4.00, "Desserts"),
    "Macaroons": MenuItem("Macaroons", 2.00, "Desserts")
    }

hour_format = namedtuple('hour_format', 'hour, meridiem') #accessing the opened and closing hours by .get(day)[0 or 1].hour and .meridiem

working_hours = {
    "Sunday": [hour_format("9:00", "AM"), hour_format("3:00", "PM")],
    "Monday": [hour_format("7:00", "AM"), hour_format("5:00", "PM")],
    "Tuesday": [hour_format("7:00", "AM"), hour_format("5:00", "PM")],
    "Wednesday": [hour_format("7:00", "AM"), hour_format("5:00", "PM")],
    "Thursday": [hour_format("7:00", "AM"), hour_format("5:00", "PM")],
    "Friday": [hour_format("7:00", "AM"), hour_format("3:00", "PM")],
    "Saturday": [hour_format("9:00", "AM"), hour_format("3:00", "PM")]
}