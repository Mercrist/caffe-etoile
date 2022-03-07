from statics import Reservation, menu
from collections import defaultdict
from tabulate import tabulate

class ShoppingCart:
    """ 
    A class that represents the current customers' shopping 
    cart. It contains their name, the current items added to the
    cart along with the items' quantity, the current subtotal, 
    and the date of a reservation if any was made.

    Attributes:
        name: A string representing the customers' name, if valid.
        cart: A dictionary containing each menu item in the cart, as string keys, along with its quantity as values.
        reservation: A reservation object, if a valid reservation is created. None otherwise
        subtotal: A float which represents the current cart's subtotal. Adjusts as items are added and removed.
    """

    def __init__(self, name:str)->None:
        """Initializes an instance of the customers' shopping cart.

        Args:
            name (str): The customers' name.

        Raises:
            TypeError: Raised if the parameters passed by the customer aren't a string.
            ValueError: Raised if the name isn't a valid string: empty or containing non-alphabetical characters.
        """
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
        self.subtotal = 0

    def __str__(self)->str:
        """Generates a string, printed to the command line, of the customers' current shopping cart.
           If there are food items in the cart, displays their: names, quantity, price,
           and finally, the current subtotal and the current reservation status.

        Returns:
            str: A string representing the state of every attribute in the shopping cart.
        """
        cart_string = "\n\n"
        if len(self.cart) < 1:
            table = f"No menu items currently in {self.name}'s cart."

        else:
            rows = []
            for item in self.cart: #creates each row in the table
                rows.append([menu.get(item).name, self.cart.get(item), f"${menu.get(item).price:.2f}"]) #item name, amount, and price

            table = tabulate(rows, headers=[self.name, "Amount", "Price"], stralign="left", numalign="center") #specifies the headers for each column

        cart_string += table + "\n\n" + f"Current subtotal: ${self.subtotal:.2f}" + "\n" + f"Reservation: {self.reservation}" + "\n\n" #format string
        return cart_string
    
    def add_items(self, item:str, amount_to_add:int=1)->None:
        """Adds a food item to the shopping cart along with the quantity the user desires to order.

        Args:
            item (str): The food item to add into the cart
            amount_to_add (int, optional): The quantity of the aforementioned item to add. Defaults to 1.

        Raises:
            TypeError: Raised if the food item to add isn't a string or if the quantity to add isn't an integer.
            ValueError: Raised if the food item isn't in the menu or if the customer attempts to add more than the minimum
                        and maximum allowed quantities of a food item.
        """
        if type(item) != str:
            raise TypeError("Menu item must be a valid string!")
        
        original_string = item #needed so that the error string returned isn't formatted
        item = item.lower()

        if not menu.get(item):
            raise ValueError(f"{original_string} does not exist on the menu!")

        if type(amount_to_add) != int:
            raise TypeError("Amount must be a whole integer!")

        if amount_to_add < 1 or amount_to_add > 10:
            raise ValueError("Attempted to add too many items in the cart!")

        if self.cart.get(item) and self.cart.get(item) + amount_to_add > 10: # verify that the amount to be added + the amount in the cart doesn't exceed the max allowed
            raise ValueError("You can't place more than 10 orders of an item!")

        self.cart[item] += amount_to_add
        self.subtotal += menu.get(item).price*amount_to_add #update the subtotal of the shopping cart as items are added or removed (no tax)

    def remove_items(self, item:str, amount_to_remove:int=1)->None:
        """Removes the given quantities of an item from the shopping cart.

        Args:
            item (str): The food item to remove from the customers' cart.
            amount_to_remove (int, optional): The amount of items to remove from the cart. Defaults to 1.

        Raises:
            TypeError: Raised if the food item to remove from the cart isn't a string or if the amount of items to remove isn't 
                        an integer.
            ValueError: Raised if the food item isn't present in the cart, if the customer attemps to remove more than the maximum 
                        or minimum allowed, or if the amount of food items to remove all is greater than the 
                        current amount of items in the cart.
        """
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

        self.subtotal -= menu.get(item).price*amount_to_remove 

    def set_reservation(self, day:str, hour:str, meridiem:str)->None:
        """Sets a cafe reservation on the given date.

        Args:
            day (str): The day of the week to set the reservation on.
            hour (str): The hour of the day, between 1 and 12, to set the reservation on.
            meridiem (str): The meridiem, AM or PM, on which the reservation will be set.
        """
        self.reservation = Reservation(day, hour, meridiem)

    def clear_reservation(self)->None:
        """If a reservation has been set by the customer, clears it out.

        Raises:
            ValueError: Raised if the customer attemps to clear an empty reservation.
        """
        if self.reservation:
            self.reservation = None

        else:
            raise ValueError("You can't clear empty reservations!")

        
class Receipt:
    pass
