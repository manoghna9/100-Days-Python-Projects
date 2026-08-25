# Day 84 - Tic Tac Toe
# A simple 2-player command-line Tic Tac Toe game

# The board contains 9 positions.
# The numbers help players know which position to choose.
board = ["1", "2", "3",
         "4", "5", "6",
         "7", "8", "9"]


def display_board():
    """Print the current game board."""

    print()
    print(f" {board[0]} | {board[1]} | {board[2]} ")
    print("---+---+---")
    print(f" {board[3]} | {board[4]} | {board[5]} ")
    print("---+---+---")
    print(f" {board[6]} | {board[7]} | {board[8]} ")
    print()


def check_winner(symbol):
    """Return True if the given symbol has won."""

    winning_combinations = [
        (0, 1, 2),  # top row
        (3, 4, 5),  # middle row
        (6, 7, 8),  # bottom row
        (0, 3, 6),  # left column
        (1, 4, 7),  # middle column
        (2, 5, 8),  # right column
        (0, 4, 8),  # diagonal
        (2, 4, 6)   # diagonal
    ]

    for combination in winning_combinations:
        first, second, third = combination

        if (board[first] == symbol and
                board[second] == symbol and
                board[third] == symbol):
            return True

    return False


def board_is_full():
    """Return True when there are no empty spaces left."""

    for position in board:
        if position not in ["X", "O"]:
            return False

    return True


def get_move(player, symbol):
    """Ask a player for a valid position."""

    while True:
        choice = input(
            f"Player {player} ({symbol}), choose a position 1-9: "
        )

        # Make sure the player entered a number.
        if not choice.isdigit():
            print("Please enter a number from 1 to 9.")
            continue

        position = int(choice)

        # Check that the number is actually on the board.
        if position < 1 or position > 9:
            print("Please choose a number between 1 and 9.")
            continue

        index = position - 1

        # Check whether somebody has already used this position.
        if board[index] in ["X", "O"]:
            print("That position is already taken. Try again.")
            continue

        board[index] = symbol
        break


def play_game():
    """Run one complete game."""

    print("\nWelcome to Tic Tac Toe!")
    print("Player 1 is X and Player 2 is O.")

    current_player = 1
    current_symbol = "X"

    while True:
        display_board()

        get_move(current_player, current_symbol)

        # Check for a winner after every move.
        if check_winner(current_symbol):
            display_board()
            print(f"🎉 Player {current_player} ({current_symbol}) wins!")
            break

        # If nobody won and the board is full, it is a draw.
        if board_is_full():
            display_board()
            print("It's a draw!")
            break

        # Switch players.
        if current_player == 1:
            current_player = 2
            current_symbol = "O"
        else:
            current_player = 1
            current_symbol = "X"


# Start the game.
play_game()