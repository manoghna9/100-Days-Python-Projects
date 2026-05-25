print("welcome to treasure island")
print("your mission is to find the treasure")
choice1 = input("you are at a cross road, where do you want to go? left or right")
if choice1 == "right":
    print("you fell into a hole. Game Over")
elif choice1 == "left":
    choice2 = input("you come to a lake. there is an island in the middle of the lake. type wait to wait for a boat. type swim to swim across")
    if choice2 == "swim":
        print("you get attacked by an angry trout. Game Over")
    elif choice2 == "wait":
        choice3 = input("you arrive at the island unharmed. there is a house with 3 doors. one red, one yellow and one blue. which colour do you choose?")
        if choice3 == "red":
            print("it's a room full of fire. Game Over")
        elif choice3 == "yellow":
            print("you found the treasure! You Win!")
        elif choice3 == "blue":
            print("you enter a room of beasts. Game Over")
        else:
            print("you chose a door that doesn't exist. Game Over")