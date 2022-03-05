from dataclasses import dataclass
from collections import namedtuple
from time import strptime   

@staticmethod
def valid_time(time:str)->bool:
    "Returns whether a given string is in a valid 12 hour time format."
    try:
        time_obj = strptime(time, '%H:%M')

    except ValueError:
        return False

    return time_obj.tm_hour <= 12 or time_obj.tm_hour >= 1

@staticmethod
def in_cafe_schedule(day: str, hour:str, meridiem:str)->bool:
    "Returns whether the working hours fit within a day or not according to the website's schedule."
    OPENING = 0 #opening and closing time offsets
    CLOSING = 1
    given_time = strptime(hour, '%H:%M')
    meridiem = meridiem.upper()
    day = day.lower()

    if given_time.tm_hour == 12: #edge case 
        return meridiem == "PM" #always open at noon!

    if meridiem == "AM": #compare only against opening hours, strictly if reservation is before opening hours
        opening_time = strptime(working_hours.get(day)[OPENING].hour, '%H:%M')  
        return given_time.tm_hour >= opening_time.tm_hour
            
    # when the meridiem is 'PM'
    closing_time = strptime(working_hours.get(day)[CLOSING].hour, '%H:%M')
    if given_time.tm_hour == closing_time.tm_hour:
        if given_time.tm_min == closing_time.tm_min:
            return given_time.tm_sec <= closing_time.tm_sec #check the minutes, a minute later we're closed

        return given_time.tm_min < closing_time.tm_min

    return given_time.tm_hour < closing_time.tm_hour

@dataclass()
class MenuItem:
    name: str
    price: float
    category: str
    description: str
    image_link: str

    def __init__(self, name:str, price:float, category:str = "", description:str = "", image_link:str = ""):
        if type(name) is not str or type(image_link) is not str or type(description) is not str:
            raise TypeError("Invalid type passed. The item's name, image link, and description should be strings!")

        if type(price) not in [int,float]:
            raise TypeError("The items price should be a number.")

        if len(name) == 0 or len(image_link) == 0 or len(description) == 0:
            raise ValueError("Empty string are not valid!")

        if price <= 0:
            raise ValueError("Items cannot be priced 0 or less!")

        
        self.name = name
        self.price = price
        self.category = category
        self.description = description
        self.image_link = image_link

@dataclass()
class Reservation:
    day: str
    hour: str
    meridiem: str

    def __init__(self, day:str, hour: str, meridiem: str):
        if type(day) != str:
            raise TypeError("Day must be a valid string! Please enter a weekday.")

        if day.lower() not in working_hours:
            raise ValueError(f"{day} is not a valid working day!")

        if type(hour) != str:
            raise TypeError("Time must be a string!")

        if not valid_time(hour):
            raise ValueError("Time must be in the 12 hour format!")

        if type(meridiem) != str:
            raise TypeError("Meridiem must be in string format!")

        if meridiem.upper() not in ['AM', 'PM'] or len(meridiem) != 2:
            raise ValueError(f"{meridiem} is not a valid meridiem! Remember meridiem means AM or PM strictly!")

        if not in_cafe_schedule(day, hour, meridiem):
            raise ValueError(f"The cafe isn't open on {day} at {hour} {meridiem}")

        self.day = day[0].upper() + day[1:].lower()
        self.hour = hour
        self.meridiem = meridiem.upper()

    def __str__(self)->str:
        return f"{self.day} at {self.hour} {self.meridiem}"

    def __eq__(self, other:'Reservation')->bool:
        return self.day == other.day and self.hour == other.hour and self.meridiem == other.meridiem

menu = {
    #coffee
    "espresso": MenuItem("Espresso", 1.00, "Coffee","The staple drink of italian origin, the espresso shot offers a strong coffee taste, showing the bean's flavors as well as leaving a nice crema on the top to enjoy.","https://bit.ly/3Ljp8xC"), 
    "cappuccino": MenuItem("Cappuccino", 3.00, "Coffee","Espresso-based drink with a nice, steamed milk foam, the cappuccino gives a soft yet rich drinking experience.","https://bit.ly/3Baw4bB"), 
    "americano": MenuItem("Americano", 2.00, "Coffee", "A diluted espresso shot, the americano looks to keep the espresso's deep flavors while softening it's strength.", "https://bit.ly/3Llk8Z8"),
    "vietnamese egg coffee": MenuItem("Vietnamese Egg Coffee", 3.00, "Specialty","Considered a delicacy in Vietnam, egg coffee combines their world class robusta beans with an egg for crema.","https://bit.ly/3oUQEbl"),
    "cuban cortadito": MenuItem("Cuban Cortadito", 3.00, "Specialty", "A small espresso shot with a cut of heated, sweetened condesed milk, taste a part of Cuban culture.", "https://bit.ly/3LtSolp"),
    "turkish coffee": MenuItem("Turkish Coffee", 3.00, "Specialty", "Coffee prepared in a cezve and prepared without filtering, experience a tradition existing since the Ottoman Empire.", "https://bit.ly/3HJ505O"), 

    #sandwiches
    "breakfast panini": MenuItem("Breakfast Panini", 7.00, "Sandwiches", "Buttered Panini bread stuffed with egg, spinach, and more.", "https://bit.ly/3gGhaR2"),
    "avocado toast": MenuItem("Avocado Toast", 5.00, "Sandwiches", "Toasted bread with slices of avocado along with whatever topping you'd like.", "https://bit.ly/3JrtTDq"),
    "blt": MenuItem("BLT", 5.00, "Sandwiches", "Bacon, Lettuce, and Tomato.", "https://bit.ly/3oNtrHL"),

    #pastries
    "french croissant": MenuItem("French Croissant", 3.00, "Pastries", "Crescent shaped delicacy, made from dough layered with butter leading to a layered, flaky texture.", "https://bit.ly/3HGS40r"),
    "puerto rican quesito": MenuItem("Puerto Rican Quesito", 2.00, "Pastries", "Rich, cheese filled puff pastry dough brushed with a simple sugar glaze.", "https://bit.ly/3Ba4gUU"),
    "mexican concha" : MenuItem("Mexican Concha", 3.00, "Pastries", "Concha's, or shell, are ubiquitous in Mexican culture coated in a cruncy topping.", "https://bit.ly/33bDn6j"), 

    #desserts
    "banana bread": MenuItem("Banana Bread", 3.00, "Desserts", "Sweet and savory bread with a crumbly texture serves a nice pair to a cup of coffee.", "https://bit.ly/3rLklNL"), 
    "new york cheesecake": MenuItem("New York Cheesecake", 4.00, "Desserts", "A staple of the big apple, comes with a reduced strawberry coating to enchance its flavor.", "https://bit.ly/3HPMQzh"),
    "macaroons": MenuItem("Macaroons", 2.00, "Desserts", "Small cakes made from almonds mixed with sugar and a grand variety of flavorings.", "https://bit.ly/3HPNiNZ")
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