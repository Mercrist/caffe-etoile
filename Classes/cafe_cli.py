from Shopping import ShoppingCart, Receipt
from Statics import menu, working_hours
from argparse import ArgumentParser
from tabulate import tabulate
from os import system,name
from pathlib import Path
import webbrowser

description = "CLI tool used to interact with Caffè Étoilé."

def generate_parser()->'ArgumentParser':
    """
    Generate an ArgumentParser object to handle user input from command line.

        Parameters:
            None
        Returns: 
            ArgumentParser object
    """
    parser = ArgumentParser(description) 
    parser.add_argument("action", help="Main action to take.",default="interactive",choices=["interactive","menu","about"],const="interactive",nargs="?")
    return parser

def interactive()->None:
    """
    Function to handle user input process. Asks users to choose whether to begin ordering,
    view the menu in their browser or exit from the program. Asks user for desired action
    from beginning to order, view the menu in their web broser,
    or simply exist the program. Internally uses get_order() and create_receipt
    function to delegate respective processes. 

        Parameters:
            None
        Returns:
            None
    """
    while True:
        clear_screen()
        user = "0"

        while user not in ["1", "2", "3"]:
            print("Welcome to Cafe Ettoile!")
            print("What would you like to do today?")
            print("1.Start ordering\n2.View menu in browser\n3.Exit")
            user = input(": ")

        if user == "1":
            view = input("Would you like to see the menu in your browser?\nNote: The browser shows more details into each specific food\n(y/n): ").lower().strip()
            if view == "y" or view == "yes":
                webbrowser.open(str(Path("../Pages/menu.html")),new=2) 
            clear_screen()
            cart = get_order()
            if not cart.cart:
                print("Thank you for visiting!")
                return
            hours = []  

            for day,window in working_hours.items():
                hours.append([day.capitalize(),f"{window[0].hour} {window[0].meridiem} - {window[1].hour} {window[1].meridiem}"]) 

            if input("Would you like to make a reservation?\n(y/n): ").lower().strip() == "y":
                while cart.reservation is None:
                    clear_screen()
                    print(tabulate(hours,headers=["Days","Hours"]))
                    day = input("\nEnter the day of your reservation:\n: ").lower().strip()
                    hour = input("\nHour of reservation\n(XX:XX format): ").lower().strip()
                    meridiem = input("\nAM or PM?\n: ").lower().strip()
                    try:
                        cart.set_reservation(day,hour,meridiem)
                    except ValueError as error:
                        print(error)
            clear_screen()
            print(cart)
            if input("Ready to checkout?\n(y/n): ") == "y":
                clear_screen()
                receipt = create_receipt(cart)
                receipt.generate_receipt()
                print("Thank you for visiting!")
                print("Generated a copy of your receipt in Classes/receipt.txt")
                return
        elif user == "2":
            webbrowser.open(str(Path("../Pages/menu.html")),new=2) 
        else:
            print("Thank you for visiting!")
            return 


def get_order()->'ShoppingCart':
    """
    Function to handle user's order information and generate a ShoppingCart object.
    Used by interactive() function above. Asks user for action to add to user's cart,
    remove an item from user's cart or head to reservation page.

        Parameters: None
        
        Returns: ShoppingCart object.
    """
    cart = None

    while cart is None:
        try:
            cart = ShoppingCart(input("Enter your name to begin: "))
        except ValueError as error:
            print(error)
        
    food_table = []
    for item in menu.values():
        food_table.append([item.name,item.price])

    while True:
        print("\n")
        print(tabulate(food_table,headers=["Item","Price"],showindex=True, tablefmt="presto"))
        print("\nItems in cart:\n")
        for item,count in cart.cart.items():
            print(f"{menu[item].name}:\t{count}")
        print(f"\nTotal in cart: {cart.subtotal:.2f}")
        print("\na.Add to cart  b.Remove from cart  c.Checkout")
        action = input(": ")
        if action.lower() == "a":
            print("What item would you like to add?")
            item = input(": ")
            try:
                if item.isnumeric():
                    item = food_table[int(item)][0]
                amount = input("Enter amount to add to order: ")
            except:
                clear_screen()
                print("\nInvalid number; be sure to use the item name or the number next to it.")
            try:
                cart.add_items(item,int(amount))
            except (ValueError, TypeError) as errors:
                print(errors)
        elif action.lower() == "b":
            print("What item would you like to remove?")
            item = input(": ")
            try:
                if item.isnumeric():
                    item = food_table[int(item)][0]
                amount = input("Enter amount to add to remove: ")
            except:
                clear_screen()
                print("\nInvalid number; be sure to use the item name or the number next to it.")
            try:
                cart.remove_items(item,int(amount))
            except (ValueError, TypeError) as errors:
                print(errors)
        elif action.lower() == "c":
            return cart
            
def create_receipt(cart: ShoppingCart)->'Receipt':
    """
    Small wrapper function to generate Receipt based from a shopping cart.

        Parameter:
            ShoppingCart: cart 

        Returns:
            Receipt object
    """
    return Receipt(
        cart.cart,
        cart.reservation,
        cart.name,
        cart.subtotal,
    )

def clear_screen():
    """
    Function to clear terminal screen for ease of reading. Taken from https://www.geeksforgeeks.org/clear-screen-python/

        Parameters:
            None
        Returns:
            None
    """
    if name == "nt":
        _ = system("cls")
    else:
        _ = system("clear")

if __name__ == "__main__":
    parser = generate_parser() 
    args = parser.parse_args()

    if args.action == "menu": 
        webbrowser.open(str(Path("../Pages/menu.html")),new=2)

    elif args.action == "interactive":
        interactive()
    
    elif args.action == "about":
        webbrowser.open(str(Path("../index.html")),new=2)