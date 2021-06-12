"""""Simple coffee machine program"""""

class Coffee:
    """Creating class coffee, with special variables for any instances"""
    def __init__(self, name, water, milk, coffee, cups, money):
        self.name = name
        self.water = water
        self.milk = milk
        self.coffee = coffee
        self.cups = cups
        self.money = money

    def ingredients_check(self):
        """A method that determines the possibility of preparing
        coffee by the remains of ingredients in the machine.
        Аnd if ingredients are enough, it makes coffee."""
        if CoffeeMachine.water < self.water:
            print("Sorry, not enough water!")
        elif CoffeeMachine.milk < self.milk:
            print("Sorry, not enough milk!")
        elif CoffeeMachine.coffee < self.coffee:
            print("Sorry, not enough coffee!")
        elif CoffeeMachine.cups < self.cups:
            print("Sorry, not enough cups!")
        else:
            print("I have enough resources, making you a coffee!")
            CoffeeMachine.water -= self.water                                   #refresh ingredients in coffee machine after creating coffee
            CoffeeMachine.milk -= self.milk
            CoffeeMachine.coffee -= self.coffee
            CoffeeMachine.cups -= self.cups
            CoffeeMachine.money += self.money                                   #adding money to machine


class CoffeeMachine:
    """Creating class of coffee machine with start ingredients in it."""
    water = 400
    milk = 540
    coffee = 120
    cups = 9
    money = 550

    @staticmethod
    def ins_print():
        """Prints how much ingredients in the coffee machine in this moment."""
        return (f"The coffee machine has:\n"
                f"{CoffeeMachine.water} of water\n"
                f"{CoffeeMachine.milk} of milk\n"
                f"{CoffeeMachine.coffee} of coffee beans\n"
                f"{CoffeeMachine.cups} of disposable cups\n"
                f"{CoffeeMachine.money} of money\n")

    @staticmethod
    def buy_coffee(num):
        """The method creates coffee by entered number of ingredients."""
        if num == "1":
            espresso = Coffee("espresso", 250, 0, 16, 1, 4)
            Coffee.ingredients_check(espresso)
        elif num == "2":
            latte = Coffee("latte", 350, 75, 20, 1, 7)
            Coffee.ingredients_check(latte)
        elif num == "3":
            cappuccino = Coffee("cappuccino", 200, 100, 12, 1, 6)
            Coffee.ingredients_check(cappuccino)

    @staticmethod
    def fill_machine():
        """Adds ingredient to the machine from the input."""
        in_water = int(input("Write how many ml of water you want to add:"))
        CoffeeMachine.water += in_water
        in_milk = int(input("Write how many ml of milk you want to add:"))
        CoffeeMachine.milk += in_milk
        in_coffee = int(input("Write how many grams of coffee beans you want to add:"))
        CoffeeMachine.coffee += in_coffee
        in_cup = int(input("Write how many disposable coffee cups you want to add:"))
        CoffeeMachine.cups += in_cup

    @staticmethod
    def take_money():
        """Allows you to take all money from the machine."""
        print(f"I gave you ${CoffeeMachine.money}")
        CoffeeMachine.money = 0


if __name__ == '__main__':
    machine = CoffeeMachine()                                                   #creating instance of coffee machine
    while True:                                                                 #opening infinite loop for our program
        choice = input("Write action (buy, fill, take, remaining, exit):")      #main menu
        if choice == "buy":
            coffee_choice = input("What do you want to buy?\
             1 - espresso, 2 - latte, 3 - cappuccino, back - to main menu:")    #sub menu
            if coffee_choice == "back":
                continue                                                        #returns you to main menu
            elif coffee_choice in ["1", "2", "3"]:
                CoffeeMachine.buy_coffee(coffee_choice)                         #makes the coffee you have chosen
            else:
                print("Wrong choice!")                                          #if your choice isn't in list
                continue                                                        #returns you to main menu
        elif choice == "fill":
            CoffeeMachine.fill_machine()                                        #adding ingredients
        elif choice == "take":
            CoffeeMachine.take_money()                                          #taking all money from the machine
        elif choice == "remaining":
            print(CoffeeMachine.ins_print())
        elif choice == "exit":                                                  #exiting the program
            break
