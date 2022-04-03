from Classes.Shopping import ShoppingCart
from Classes.Shopping import Receipt
from collections import defaultdict

def json_to_cart(json:dict) -> ShoppingCart:
    cart = ShoppingCart(json.get('name','user'))
    cart.cart = defaultdict(int,json['cart'])
    cart.reservation = json['reservation']
    cart.subtotal = json['subtotal']

    return cart 

def receipt_to_json(receipt: Receipt):
    return {
        "name" : receipt.name,
        "subtotal" : receipt.subtotal,
        "total" : receipt.total(),
        "receipt_number" : receipt.receipt_number(),
        "food_items" : receipt.food_items,
        "tax_percent" : receipt.tax_percent,
        "reservation" : str(receipt.reservation)
    }