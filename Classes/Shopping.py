from datetime import datetime, timezone
from .Statics import Reservation, menu   
from collections import defaultdict
from tabulate import tabulate
import hashlib
from dataclasses import dataclass

@dataclass
class ShoppingCart:
    """ 
    A class that represents the customers' shopping 
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
            menu_rows = []
            for item, quantity in self.cart.items(): #creates each row in the table
                menu_rows.append([menu.get(item).name, quantity, f"${menu.get(item).price:.2f}"]) #item name, amount, and price

            table = tabulate(menu_rows, headers=[self.name, "Amount", "Price"], stralign="left", numalign="center") #specifies the headers for each column

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
    """ 
    A class that represents the customers' order receipt. Based
    on their final order after payment, contains all information 
    based on their order info: the items and quantities purchased,
    the reservation date if any was made, the customers' name, and
    their subtotal.

    Attributes:
        items: A dictionary containing each food item from their order, as string keys, and their quantities as integer values.
        reservation: A reservation object containing the date of the reservation, or None if a reservation wasn't set.
        name: A string, representing a valid customer name.
        subtotal: A float which represents the final subtotal. Items ordered cannot be changed.
        tax_percent: A float which represents the sales tax rate for the cafe.
    """

    def __init__(self, food_items:dict, reservation:'Reservation', name:str, subtotal:float)->None:
        """Initializes an instance of a receipt object.

        Args:
            items (dict): Contains the items in the final order as key strings and their quantities as integer values.
            reservation (Reservation): Contains the date of the reservation. None if a reservation wasn't set.
            name (str): Represents the customers' name.
            subtotal (float): Contains the final subtotal. Items ordered cannot be changed.

        Raises:
            TypeError: Raised if the food items aren't in a dictionary, if the reservation is not a valid Reservation object,
                       the customer name isn't a string, or the subtotal isn't a float or integer.

            ValueError: Raised if the food items' dictionary is empty or contains invalid keys or values, the customer name contains 
                        non alphanumeric characters or is empty, or if the subtotal is less than or equals to zero. All orders
                        must have a positive, non zero subtotal.
        """
        if type(food_items) not in [dict, defaultdict]:
            raise TypeError(f"Items must be a dictionary. Given type: {type(food_items)}")
            
        if type(reservation) is not Reservation and reservation is not None: #Reservations can be None
            raise TypeError(f"Error: Reservations must be Reservation type. Given type: {type(reservation)}")

        if type(name) is not str:
            raise TypeError(f"Error: name must be a string. Given type: {type(name)}")

        if type(subtotal) not in [int, float]:
            raise TypeError(f"Error: Total is not a number type. Given type: {type(subtotal)}")

        if not food_items or None in food_items.values() or sum(1 for amount in food_items.values() if amount < 0):
            raise ValueError("Error: Cannot generate receipt of no items.")

        if not name or not name.split():
            raise ValueError("Error: Customer name must not be empty")

        for letter in name.split():
            if not letter.isalpha() or letter.isspace():
                raise ValueError("Error: Customer name must not have special characters or numbers.")

        if subtotal <= 0:
            raise ValueError("Cannot make a receipt for a purchase with no total or a purchase with a sub zero total!")

        self.food_items = food_items
        self.reservation = reservation
        self.name = name 
        self.subtotal = subtotal 
        self.tax_percent = 10.25/100

    def tax(self)->float:
        """Calculates the sales tax amount for the given orders' subtotal.

        Returns:
            float: The sales tax of the customers' order, rounded up to two decimal places.
        """
        return round(self.subtotal * self.tax_percent, 2)

    def total(self)->float:
        """Calculates the customers' final order total. By definition, 
           the final total is the sum of the order subtotal combined
           with its corresponding sales tax.

        Returns:
            float: The final total of the customers' order.
        """
        return self.subtotal + self.tax() 

    def receipt_number(self)->str: 
        """Generates a 10 digit receipt number for the current order. 
           Every receipt must have a unique, corresponding receipt number 
           which can be recreated given the customers' order info.
           Generated by taking the first four digits of the customers'
           name hash, the first three digits of the total order's value in
           pennies, and the number of unique items ordered. 
        
        Returns:
            str: The current receipts' unique receipt number, as a string. 
        """

        def simple_hash(name:str)->str:
            """Calculates a simple hash given a string using RSA's MD5 
               algorithm. Unlike the built in hash function, this guarantees
               a constant hash across sessions.

            Args:
                name (str): The input string to be hashed. For the receipt's purposes, it's the customers' name.

            Returns:
                str: A string representing the first four digits of the resulting hash.
            """
            name = name.encode("utf-8") #encode for string hashing
            md5_hash = hashlib.md5()
            md5_hash.update(name)
            return str(int(md5_hash.hexdigest(), 16))[:4] #converts to hex, converts to the equivalent int, gets first four digits
        
        def to_pennies(order_total:float)->str:
            """Converts the order's total from USD to pennies.
               Since the cheapest item in the menu is a dollar, 
               this is always guaranteed to be at least three digits
               long.

            Args:
                order_total (float): The final orders' total, in USD.

            Returns:
                str: The final orders' total in pennies, as a string.
            """
            return str(order_total * 100)[:3] #converting usd to pennies and getting the first three digits

        def first_three_length_cart(items_ordered:int)->str:
            """Calculates the final three digits in the receipt number
               by getting the amount of unique items ordered. 
               If this amount is less than three, fills in the 
               remaining digits to the left with zeros.

            Args:
                items_ordered (int): The number of unique items ordered, not their quantity.

            Returns:
                str: The number of unique items ordered, formatted as a string. If this amount is less
                     than three, fills in the remaining spots with zeros.
            """
            items_ordered = str(items_ordered)

            if len(items_ordered) < 3:
                items_ordered = items_ordered.zfill(3) #fill as many remaining spots with zero (1 or 2 zeros)

            return items_ordered[:3]

        #calculates the receipt number
        name_hash = simple_hash(self.name)
        pennies = to_pennies(self.total())
        length = first_three_length_cart(len(self.food_items))

        return name_hash + pennies + length

    def generate_receipt(self)->None:
        """Writes the final receipt to a text file within the current directory.
           Displays the receipt's attributes, orders, and more such as: 
           items ordered with their quantities, the totals, the receipt number, 
           the time at which the order was placed, the customer's name, 
           and the reservation date.
        """
        receipt_string = "CAFFÈ ÉTOILÉ\n"

        receipt_rows = []
        for food_order, quantity in self.food_items.items():
            receipt_rows.append([menu.get(food_order.lower()).name, quantity, f"${menu.get(food_order.lower()).price:.2f}"]) #item name, amount, and price
        
        receipt_body = tabulate(
            receipt_rows,
            headers=["Items", "Amount", "Price"], 
            stralign="left",
            numalign="center",
            tablefmt="psql"
        )
        
        receipt_string += receipt_body + "\n\n"

        #Price calculations
        to_pay_rows = [["Subtotal: ", f"${self.subtotal:.2f}"], ["Tax: ", f"${self.tax():.2f}"], ["Total: ", f"${self.total():.2f}"]]
        payments = tabulate(
            to_pay_rows,
            stralign="left",
            numalign="left",
            tablefmt="simple"
        )

        utc_now = datetime.now(timezone.utc) #gets the current time in utc
        local_time_obj = utc_now.astimezone() #gets the specific utc timezone (from the computer system)
        time_string = local_time_obj.strftime("%m-%d-%Y at %I:%M %p") #get current/local time as 12-hour string

        receipt_string += payments + "\n\n" + f"Customer: {self.name}\n" + f"Receipt Number: #{self.receipt_number()}\n" + f"Reservation: {self.reservation}\n" \
                         f"Time Generated: {time_string}\n\n" + "Thanks for stopping by!" 

        with open("receipt.txt", "w", encoding='utf-8') as receipt_file: #write receipt to text file, utf-8 for special characters
            receipt_file.write(receipt_string)
        