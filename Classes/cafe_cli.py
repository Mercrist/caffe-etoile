from Shopping import ShoppingCart, Receipt
from argparse import ArgumentParser
from Statics import Reservation, menu, working_hours
from tabulate import tabulate
import webbrowser

description = "CLI tool used to interact with Caffè Étoilé."

def generate_parser() -> ArgumentParser:
    """
    Generate an ArgumentParser object to handle user input from command line.
    """
    parser = ArgumentParser(description) 
    parser.add_argument("action", help="Main action to take.",default="interactive",choices=["interactive","menu","reservation","about"])
    return parser

def interactive() -> None:
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
    print("Welcome to Cafe Ettoile!")
    print("What would you like to do today?")
    print("1.Start ordering\n2.View menu\n3.Exit")
    user = input(": ")
    if user == "1":
        view = input("Would you like to see the menu in your browser?\nNote: The browser shows more details into each specific food\n(y/n): ").lower()
        if view == "y" or view == "yes":
            webbrowser.open("../Pages/menu.html",new=2) 
        cart = get_order()
        hours = []   
        for day,window in working_hours.items():
            hours.append([day,f"{window[0].hour} {window[0].meridiem} - {window[1].hour} {window[1].meridiem}"]) 

        while cart.reservation is None:
            print(tabulate(hours,headers=["Days","Hours"]))
            day = input("\nEnter the day of your reservation:\n: ").lower().strip()
            hour = input("\nHour of reservation\n(XX:XX format): ").lower().strip()
            meridiem = input("\nAM or PM?\n: ").lower().strip()
            try:
                cart.set_reservation(day,hour,meridiem)
            except ValueError:
                print("Sorry, one of your inputs wasn't correct. Try again!")
        print(cart)
        if input("Ready to checkout?]\n(y/n): ") == "y":
            receipt = create_receipt(cart)
            receipt.generate_receipt()
            print("Thank you for visiting!")
            print("Generated a copy of your receipt in Classes/receipt.txt")
    elif user == "2":
        webbrowser.open("../Pages/menu.html",new=2) 
    else:
        print("Thank you for visiting!")
        return 


def get_order() -> ShoppingCart:
    """
    Function to handle user's order information and generate a ShoppingCart object.
    Used by interactive() function above. Asks user for action to add to user's cart,
    remove an item from user's cart or head to reservation page.

        Parameters: None
        
        Returns: ShoppingCart object.
    """
    cart = ShoppingCart(input("Enter your name to begin: "))
    food_table = []
    for item in menu.values():
        food_table.append([item.name,item.price])

    while True:
        print(tabulate(food_table,headers=["Item","Price"],showindex=True, tablefmt="presto"))
        print("\nItems in cart:")
        for item,count in cart.cart.items():
            print(f"{item}:\t{count}")
        print(f"\nTotal in cart: {cart.subtotal:.2f}")
        print("\na. Add to cart\t b.Remove from cart\t c.Reservation and Checkout")
        action = input(": ")
        if action.lower() == "a":
            print("What item would you like to add?")
            item = input(": ")
            if item.isnumeric():
                item = food_table[int(item)][0]
            amount = int(input("Enter amount to add to order: "))
            try:
                cart.add_items(item,amount)
            except ValueError:
                print("Sorry, that item isn't available on the menu. Try again!")
        elif action.lower() == "b":
            print("What item would you like to remove?")
            item = input(": ")
            if item.isnumeric():
                item = food_table[int(item)][0]
            amount = int(input("Enter amount to add to remove: "))
            try:
                cart.remove_items(item,amount)
            except ValueError:
                print("Sorry, that item isn't available on the menu. Try again!")
        elif action.lower() == "c":
            return cart
            
def create_receipt(cart: ShoppingCart) -> Receipt:
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


if __name__ == "__main__":
    parser = generate_parser() 
    args = parser.parse_args()

    if args.action == "menu": 
        webbrowser.open("../Pages/menu.html",new=2)

    elif args.action == "interactive":
        interactive() 
    
    elif args.action == "about":
        webbrowser.open("../index.html",new=2)