from dataclasses import dataclass


@dataclass()
class MenuItem:
    name: str
    price: int
    image_link: str
    description: str

    def __init__(self, name:str, price:int, image_link:str, description:str):
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


