from dataclasses import dataclass
from time import strptime
import data

@staticmethod
def validTime(time:str)->bool:
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
    image_link: str
    description: str

    def __init__(self, name:str, price:int, description:str = "", category:str = "", image_link:str = ""):
        if type(name) is not str or type(image_link) is not str or type(description) is not str:
            raise TypeError("Invalid type passed. The item's name, image link and description should be strings!")
        if type(price) is not int:
            raise TypeError("The items price should be an int.")
        if len(name) == 0 or len(image_link) == 0 or len(description) == 0:
            raise ValueError("Empty string are not valid! Check that values aren't empty")
        if price <= 0:
            raise ValueError("Items cannot be priced 0 or less!")
        
        self.name = name 
        self.price = price
        self.image_link = image_link
        self.description = description

@dataclass()
class Reservation:
    day: str
    hour: str
    meridiem: str

    def __init__(self, day:str, hour: str, meridiem: str):
        if type(day) != str:
            raise TypeError("Day must be a valid string! Please enter a weekday.")

        if day not in data.working_hours:
            raise ValueError("Not a valid working day!")

        if type(hour) != str:
            raise TypeError("Time must be a string!")

        if not validTime(hour):
            raise ValueError("Time must be in the 12 hour format!")

        if type(meridiem) != str:
            raise TypeError("Meridiem must be in string format!")

        if meridiem.upper() not in ['AM', 'PM'] or len(meridiem) != 2:
            raise ValueError("Not a valid meridiem! Remember meridiem means AM or PM strictly!")

        if not in_cafe_schedule(day, hour, meridiem):
            raise ValueError("The cafe isn't open during these hours!")

        self.day = day 
        self.hour = hour
        self.meridiem = meridiem