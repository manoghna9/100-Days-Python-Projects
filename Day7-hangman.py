import random

word_list = ["apple", "tiger", "mango", "python"]

chosen_word = random.choice(word_list)

print("The chosen word is " + chosen_word)

placeholder = ""

for position in range(len(chosen_word)):
    placeholder += "_"

print(placeholder)

game_over = False

display = placeholder

while not game_over:

    guess = input("Guess a letter: ").lower()

    new_display = ""

    for position in range(len(chosen_word)):

        letter = chosen_word[position]

        if letter == guess:
            print("Right")
            new_display += letter

        else:
            print("Wrong, try again")
            new_display += display[position]

    display = new_display

    print(display)

    if "_" not in display:
        game_over = True
        print("You win!")