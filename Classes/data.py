from statics import MenuItem

foods = {
    #coffee
    "Espresso": MenuItem("Espresso", 1.00, "Coffee"), 
    "Cappuccino": MenuItem("Cappuccino", 3.00, "Coffee"), 
    "Americano": MenuItem("Americano", 2.00, "Coffee"),
    "Vietnamese Egg Coffee": MenuItem("Vietnamese Egg Coffee", 3.00, "Specialty"),
    "Cuban Cortadito": MenuItem("Cuban Cortadito", 3.00, "Specialty"),
    "Turkish Coffee": MenuItem("Turkish Coffee", 3.00, "Specialty"), 

    #sandwiches
    "Breakfast Panini": MenuItem("Breakfast Panini", 7.00, "Sandwiches"),
    "Avocado Toast": MenuItem("Avocado Toast", 5.00, "Sandwiches"),
    "BLT": MenuItem("BLT", 5.00, "Sandwiches"),

    #pastries
    "French Croissant": MenuItem("French Croissant", 3.00, "Pastries"),
    "Puerto Rican Quesito": MenuItem("Puerto Rican Quesito", 2.00, "Pastries"),
    "Mexican Concha" : MenuItem("Mexican Concha", 3.00, "Pastries"), 

    #desserts
    "Banana Bread": MenuItem("Banana Bread", 3.00, "Desserts"), 
    "New York Cheesecake": MenuItem("New York Cheesecake", 4.00, "Desserts"),
    "Macaroons": MenuItem("Macaroons", 2.00, "Desserts")
    }

working_hours = {}