from collections import namedtuple
from dataclasses import dataclass
from time import strptime 
from config import Config
import pymongo

def valid_time(time:str)->bool:
    """Determines whether the input parameter is in the cafe's requested, 12-hour time format.

    Args:
        time (str): The time format to verify, from 1:00 up to and including 12:00.

    Returns:
        bool: True, if time is a valid 12-hour, time format. False otherwise.
    """
    try:
        time_obj = strptime(time, '%H:%M')

    except ValueError:
        return False

    return time_obj.tm_hour <= 12 and time_obj.tm_hour >= 1

def in_cafe_schedule(day:str, hour:str, meridiem:str)->bool:
    """Determines whether the given reservation fields are within the cafe's opening and closing hours.
       All parameters are validated within the reservation class's constructor beforehand.

    Args:
        day (str): The given day of the week.
        hour (str): The hour, in 12-hour format, at which the reservation is to be made.
        meridiem (str): AM or PM, and used in conjunction with the hour in order to verify whether the reservation day
                        fits within the cafe's schedule.

    Returns:
        bool: True, if the given date and time is within the cafe's opening and closing hours. False otherwise.
    """
    OPENING = 0 #opening and closing time offsets
    CLOSING = 1
    given_time = strptime(hour, '%H:%M')
    meridiem = meridiem.upper()
    day = day.lower()

    if given_time.tm_hour == 12:
        return meridiem == "PM" #edge case, never open at midnight, always open at noon

    if meridiem == "AM": #compare only against opening hours, strictly if reservation is before opening hours
        opening_time = strptime(working_hours.get(day)[OPENING].hour, '%H:%M')  
        return given_time.tm_hour >= opening_time.tm_hour
            
    # when the meridiem is 'PM' and after noon
    closing_time = strptime(working_hours.get(day)[CLOSING].hour, '%H:%M')
    if given_time.tm_hour == closing_time.tm_hour: #if the hours are the same, check the minutes
        if given_time.tm_min == closing_time.tm_min:
            return given_time.tm_sec <= closing_time.tm_sec #minute later after the closing time

        return given_time.tm_min < closing_time.tm_min

    return given_time.tm_hour < closing_time.tm_hour
    

@dataclass()
class MenuItem:
    """An immutable data class which instintiates a cafe menu item.
       Allows for quick retrieval of an items' attributes.

    Attributes:
        name: A string, representing the menu items' name, with proper punctuation.
        price: The price of a menu item, in USD, as a float.
        category: The menu category to which the item belongs to, as a string.
        description: Flavor text describing the menu item, as a string.
        image_link: A string containing the image link for the food item, as displayed on the website.
    """
    name: str
    price: float
    category: str
    description: str
    image_link: str

    def __init__(self, name:str, price:float, category:str = "specialty", description:str = "N/A", image_link:str = "invalid_link"):
        """Initializes an instance of a cafe menu item.

        Args:
            name (str): A valid menu item name.
            price (float): The non-zero, positive price of the menu item.
            category (str, optional): The menu category the food belongs to. Defaults to the specialty category.
            description (str, optional): The food item description, as shown on the cafe's website. Defaults to "Not Applicable".
            image_link (str, optional): The image link for the food item, as displayed on the cafe's website. Defaults to placeholder text.

        Raises:
            TypeError: Raised if none of the parameters are strings, with the exception of the menu item price which must be a float.
            ValueError: Raised if any of the string categories are empty, the price is unreasonable or invalid, or the food category
                        is not a valid menu category.
        """
        if type(name) is not str or type(category) is not str or type(image_link) is not str or type(description) is not str:
            raise TypeError("Invalid type passed. The item's name, image link, and description should be strings!")

        if type(price) not in [int,float]:
            raise TypeError("The items price should be a number.")

        if not name.split() or not category.split() or not description.split() or not image_link.split():
            raise ValueError("Empty string are not valid!")

        if price <= 0:
            raise ValueError("Items cannot be priced 0 or less!")

        if price >= 50: #arbitrary value
            raise ValueError("Excessive pricing")

        if category.lower() not in ["specialty","coffee","desserts","sandwiches","pastries"]:
            raise ValueError("Not a valid category")
        
        self.name = name
        self.price = price
        self.category = category
        self.description = description
        self.image_link = image_link

@dataclass()
class Reservation:
    """An immutable data class containing information
       pertaining to the exact date a customer sets
       a cafe reservation.

    Attributes:
        day: A string representing the day of the week at which the customer desires to set the reservation.
        hour: The hour, as a 12-hour format string, at which to set the reservation.
        meridiem: A string denoting whether the time of the reservation shall be at AM or PM. 
                  Must be within the cafe's opening and closing hours.
    """
    day:str
    hour:str
    meridiem:str

    def __init__(self, day:str, hour:str, meridiem:str)->None:
        """Initializes an instance of a cafe reservation.

        Args:
            day (str): The day of the week to set the reservation.
            hour (str): The hour of the day, between 1 and 12, to set the reservation on.
            meridiem (str): The meridiem, AM or PM, on which the reservation will be set.

        Raises:
            TypeError: Raised if the day, hour, or meridiem aren't strings.
            ValueError: Raised if the day isn't a day of the week, the hour isn't between 1:00-12:00, the
                        meridiem isn't AM or PM, or if the date provided is outside of the cafe's opening 
                        and closing hours.
        """
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
        """Generates a string, printed to the command line, which displays the exact date of the current 
           customers' reservation.

        Returns:
            str: A string, displaying the exact date of the current reservation.
        """
        return f"{self.day} at {self.hour} {self.meridiem}"

    def __eq__(self, other:'Reservation')->bool:
        """Compares two reservation objects by checking if their attributes are the same.

        Args:
            other (Reservation): The reservation object to compare to the current instance.

        Returns:
            bool: True, if the current instance and the parameter reservation object are the same. False otherwise.

        Raises:
            TypeError: Raised if the parameter isn't a Reservation object.
        """
        if type(other) != Reservation:
            raise TypeError("Object to compare must be a valid Reservation object!")

        return self.day == other.day and self.hour == other.hour and self.meridiem == other.meridiem

'Local database values'
menu = {
    #coffee
    "espresso": MenuItem("Espresso", 1.00, "Coffee","The staple drink of italian origin, the espresso shot offers a strong coffee taste, showing the bean's flavors as well as leaving a nice crema on the top to enjoy.","https://bit.ly/3Ljp8xC"), 
    "cappuccino": MenuItem("Cappuccino", 3.00, "Coffee","Espresso-based drink with a nice, steamed milk foam, the cappuccino gives a soft yet rich drinking experience.","https://bit.ly/3Baw4bB"), 
    "americano": MenuItem("Americano", 2.00, "Coffee", "A diluted espresso shot, the americano looks to keep the espresso's deep flavors while softening it's strength.", "https://bit.ly/3Llk8Z8"),
    "vietnamese egg coffee": MenuItem("Vietnamese Egg Coffee", 3.00, "Specialty","Considered a delicacy in Vietnam, egg coffee combines their world class robusta beans with an egg for crema.","https://bit.ly/3oUQEbl"),
    "cuban cortadito": MenuItem("Cuban Cortadito", 3.00, "Specialty", "A small espresso shot with a cut of heated, sweetened condesed milk, taste a part of Cuban culture.", "https://bit.ly/3LtSolp"),
    "turkish coffee": MenuItem("Turkish Coffee", 3.00, "Specialty", "Coffee prepared in a cezve and prepared without filtering, experience a tradition existing since the Ottoman Empire.", "https://bit.ly/3HJ505O"), 
    "matcha": MenuItem("Matcha", 5.00, "Specialty", "Japanese green tea made from the Camellia sinensis plant. Its dried leaves and leaf buds are used to make several different teas, including black and oolong teas.", "https://bit.ly/3La0K0o"), 

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

hour_format = namedtuple('hour_format', 'hour meridiem') #accessing the opened and closing hours by .get(day)[0 or 1].hour and .meridiem

working_hours = {
    "sunday": [hour_format("9:00", "AM"), hour_format("3:00", "PM")],
    "monday": [hour_format("7:00", "AM"), hour_format("5:00", "PM")],
    "tuesday": [hour_format("7:00", "AM"), hour_format("5:00", "PM")],
    "wednesday": [hour_format("7:00", "AM"), hour_format("5:00", "PM")],
    "thursday": [hour_format("7:00", "AM"), hour_format("5:00", "PM")],
    "friday": [hour_format("7:00", "AM"), hour_format("3:00", "PM")],
    "saturday": [hour_format("9:00", "AM"), hour_format("3:00", "PM")]
}

def reset_menu_collection()->None:
    """Helps refactor the cafe menu into the online DB.
       Resets the documents in the online DB and replaces 
       them with the local database.
    """
    config = Config()
    client = pymongo.MongoClient(config.MONGO_URI)
    db = client.database
    db_menu = db.menu
    db_menu.delete_many({})

    for item_obj in menu.values():
        food_entry = {
            "name": item_obj.name,
            "price": item_obj.price,
            "category": item_obj.category,
            "description": item_obj.description,
            "image_link": item_obj.image_link
        }
        db_menu.insert_one(food_entry) #inserts the document into the mongodb database