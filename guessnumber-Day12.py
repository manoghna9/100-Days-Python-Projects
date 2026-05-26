from random import randint

# Function to check user's guess against actual answer
def check_answer(user_guess, actual_answer, turns):
    if user_guess > actual_answer:
        print("Too high.")
        return turns - 1
    elif user_guess < actual_answer:
        print("Too low.")
        return turns - 1
    else:
        print(f"You got it! The answer was {actual_answer}.")

# Function to set difficulty
def set_difficulty():
    level = input("Choose a difficulty. Type 'easy' or 'hard': ")

    if level == "easy":
        return 10
    else:
        return 5


# Choosing a random number between 1 and 100
print("Welcome to the Number Guessing Game!")
print("I'm thinking of a number between 1 and 100.")

answer = randint(1, 100)

# Set difficulty
turns = set_difficulty()

# Repeat the guessing functionality if they get it wrong
game_over = False

while not game_over:

    print(f"You have {turns} attempts remaining to guess the number.")

    # Let the user guess a number
    guess = int(input("Make a guess: "))

    # Track the number of turns and reduce by 1 if they get it wrong
    turns = check_answer(guess, answer, turns)

    if guess == answer:
        game_over = True
    elif turns == 0:
        print("You've run out of guesses. You lose.")
        print(f"The answer was {answer}")
        game_over = True
    else:
        print("Guess again.\n")