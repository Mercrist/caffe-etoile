from argparse import ArgumentParser
import webbrowser
from Classes.Shopping import ShoppingCart,Receipt
from Classes.statics import menu
from tabulate import tabulate


description = "CLI tool used to interact with Caffè Étoilé."

def generate_parser():
    parser = ArgumentParser(description) 
    parser.add_argument("action", help="Main action to take.",default="interactive",choices=["interactive","menu","reservation","about"])
    return parser

def interactive():
    print("Welcome to Cafe Ettoile!")
    print("What would you like to do today?")
    print("1.Start ordering\n2.View reservation\n3.Exit")
    user = input(": ")
    if user == "1":
        view = input("Would you like to see the menu in your browser?\nNote: The browser shows more details into each specific food\n(y/n): ").lower()
        if view == "y" or view == "yes":
            webbrowser.open("Pages/menu.html",new=2) 
        cart = get_order()   
        reservation = get_reservation() 
    elif user == "2":
        reservation = input("Enter your receipt number to view your reservation")
    else:
        print("Thank you for visiting!")
        return 

def get_reservation():
    pass

def get_order():
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
        print("\na. Add to cart\t b.Remove from cart\t c.Exit")
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
            



if __name__ == "__main__":
    parser = generate_parser() 
    args = parser.parse_args()

    if args.action == "menu": 
        webbrowser.open("Pages/menu.html",new=2)

    elif args.action == "interactive":
        interactive() 
    
    elif args.action == "about":
        webbrowser.open("index.html",new=2)