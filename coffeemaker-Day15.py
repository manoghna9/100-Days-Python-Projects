MENU = {
    "espresso": {
        "ingredients": {
            "water": 50,
            "coffee": 18,
        },
        "cost": 1.5,
    },

    "latte": {
        "ingredients": {
            "water": 200,
            "milk": 150,
            "coffee": 24,
        },
        "cost": 2.5,
    },

    "cappuccino": {
        "ingredients": {
            "water": 250,
            "milk": 100,
            "coffee": 24,
        },
        "cost": 3.0,
    }
}


resources = {
    "water": 300,
    "milk": 200,
    "coffee": 100,
}

money = 0


# Function to check resources
def is_resource_sufficient(order_ingredients):
    for item in order_ingredients:
        if order_ingredients[item] > resources[item]:
            print(f"Sorry there is not enough {item}.")
            return False
    return True


# Function to process coins
def process_coins():
    print("Please insert coins.")
    
    quarters = int(input("How many quarters?: "))
    dimes = int(input("How many dimes?: "))
    nickles = int(input("How many nickles?: "))
    pennies = int(input("How many pennies?: "))

    total = (quarters * 0.25) + (dimes * 0.10) + (nickles * 0.05) + (pennies * 0.01)

    return total


# Function to check payment
def is_transaction_successful(money_received, drink_cost):
    global money

    if money_received < drink_cost:
        print("Sorry that's not enough money. Money refunded.")
        return False

    change = round(money_received - drink_cost, 2)
    print(f"Here is ${change} in change.")

    money += drink_cost
    return True


# Function to make coffee
def make_coffee(drink_name, order_ingredients):
    for item in order_ingredients:
        resources[item] -= order_ingredients[item]

    print(f"Here is your {drink_name} ☕ Enjoy!")


# Main program
machine_on = True

while machine_on:

    choice = input("What would you like? (espresso/latte/cappuccino): ").lower()

    # Turn off machine
    if choice == "off":
        machine_on = False

    # Print report
    elif choice == "report":
        print(f"Water: {resources['water']}ml")
        print(f"Milk: {resources['milk']}ml")
        print(f"Coffee: {resources['coffee']}g")
        print(f"Money: ${money}")

    # Coffee options
    elif choice in MENU:

        drink = MENU[choice]

        # Check resources
        if is_resource_sufficient(drink["ingredients"]):

            # Process coins
            payment = process_coins()

            # Check payment
            if is_transaction_successful(payment, drink["cost"]):

                # Make coffee
                make_coffee(choice, drink["ingredients"])

    else:
        print("Invalid choice.")