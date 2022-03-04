from statics import Reservation, menu
from collections import defaultdict
from tabulate import tabulate

class ShoppingCart:
    def __init__(self, name:str):
        if type(name) != str:
            raise TypeError("Customer name must be a string!")

        if not name or not name.strip():
            raise ValueError("Customer name cannot be empty!")
        
        for names in name.split():
            if not names.isalpha():
                raise ValueError("Customer name must not have special characters or numbers!")

        self.name = name
        self.cart = defaultdict(int) #keys are strings of the menu item and values are the amount of orders of that item
        self.reservation = None
        self.total_cost = 0

    def __str__(self):
        cart_string = "\n\n"
        if len(self.cart) < 1:
            table = f"No menu items currently in {self.name}'s cart."

        else:
            rows = []
            for item in self.cart:
                rows.append([menu.get(item).name, self.cart.get(item), f"${menu.get(item).price:.2f}"]) #item name, amount, and price

            table = tabulate(rows, headers=[self.name, "Amount", "Price"], stralign="left", numalign="center") #specifies the headers for each column

        cart_string += table + "\n\n" + f"Current subtotal: ${self.total_cost:.2f}" + "\n" + f"Reservation: {self.reservation}" + "\n\n"
        return cart_string
    
    def add_items(self, item:str, amount:int=1)->None:
        if type(item) != str:
            raise TypeError("Menu item must be a valid string!")
        
        original_string = item #such that the error string returned isn't formatted
        item = item.lower()

        if not menu.get(item):
            raise ValueError(f"{original_string} does not exist on the menu!")

        if type(amount) != int:
            raise TypeError("Amount must be a whole integer!")

        if amount < 1 or amount > 10:
            raise ValueError("Attempted to add too many items in the cart!")

        if self.cart.get(item) and self.cart.get(item) + amount > 10:
            raise ValueError("You can't place more than 10 orders of an item!")

        self.cart[item] += amount
        self.total_cost += menu.get(item).price*amount #update the total cost of the shopping cart as items are added or removed (no tax)

    def remove_items(self, item:str, amount_to_remove:int=1)->None:
        if type(item) != str: # Verifying if item to add is valid
            raise TypeError(f"The item to be removed must be a string!")

        original_string = item 
        item = item.lower()

        if item not in self.cart:
            raise ValueError(f"{original_string} is not currently in the cart!")

        # Verifying if the amount to remove is valid and its edge cases
        amount_in_cart = self.cart.get(item)
        
        if type(amount_to_remove) != int:
            raise TypeError("The amount of items to be removed must be a whole integer!")

        if amount_to_remove < 1 or amount_to_remove > 10:
            raise ValueError("Can't remove more items than the maximum or minimum allowed!")
    
        if amount_to_remove > amount_in_cart:
            raise ValueError("Can't remove more items than currently present in the cart!")

        if amount_to_remove == amount_in_cart:
            del self.cart[item]

        else:
            self.cart[item] -= amount_to_remove

        self.total_cost -= menu.get(item).price*amount_to_remove 

    def set_reservation(self, day:str, hour:str, meridiem:str)->None:
        self.reservation = Reservation(day, hour, meridiem)

    def clear_reservation(self)->None:
        if self.reservation:
            self.reservation = None

        else:
            raise ValueError("You can't clear empty reservations!")

        
class Receipt:
    pass
