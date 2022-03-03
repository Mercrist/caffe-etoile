from dataclasses import dataclass
from time import strptime
from collections import namedtuple



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

    if meridiem == "AM": #compare only against opening hours, strictly if reservation is before opening hours
        opening_time = strptime(data.working_hours.get(day)[OPENING].hour, '%H:%M')  
        return given_time.tm_hour >= opening_time.tm_hour
            
    # when the meridiem is 'PM'
    closing_time = strptime(data.working_hours.get(day)[CLOSING].hour, '%H:%M')
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

    def __init__(self, name:str, price:int, category:str = "", description:str = "", image_link:str = ""):
        if type(name) is not str or type(image_link) is not str or type(description) is not str:
            raise TypeError("Invalid type passed. The item's name, image link and description should be strings!")

        if type(price) is not int:
            raise TypeError("The items price should be an int.")

        if len(name) == 0 or len(image_link) == 0 or len(description) == 0:
            raise ValueError("Empty string are not valid!")

        if price <= 0:
            raise ValueError("Items cannot be priced 0 or less!")

        if name not in menu:
            raise ValueError(f"{name} isn't on the menu!")
        
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

        if day.lower() not in data.working_hours:
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

        self.day = self.day[0].upper() + self.day[1:].lower()
        self.hour = hour
        self.meridiem = meridiem.upper()

    def __str__(self):
        return f"{self.day} at {self.hour} {self.meridiem}"


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