from Classes.Shopping import ShoppingCart
from collections import defaultdict
def json_to_cart(json:dict) -> ShoppingCart:
    cart = ShoppingCart(json.get('name','user'))
    cart.cart = defaultdict(int,json['cart'])
    cart.reservation = json['reservation']
    cart.subtotal = json['subtotal']

    return cart 