import turtle
import pandas as pd

# setup screen and map image
screen = turtle.Screen()
screen.title("U.S. States Game")

image = "blank_states_img.gif"

screen.addshape(image)
turtle.shape(image)

# read csv data
data = pd.read_csv("50_states.csv")

# convert states column into list
all_states = data.state.to_list()

# stores correct guesses
guessed_states = []

# main game loop
while len(guessed_states) < 50:

    answer_state = screen.textinput(
        title=f"{len(guessed_states)}/50 States Correct",
        prompt="Enter a state name:"
    )

    if answer_state is None:
        break

    answer_state = answer_state.title()

    # creates csv of missing states if user exits
    if answer_state == "Exit":

        missing_states = []

        for state in all_states:

            if state not in guessed_states:
                missing_states.append(state)

        new_data = pd.DataFrame(missing_states)

        new_data.to_csv("states_to_learn.csv")

        break

    # checks if answer is correct
    if answer_state in all_states and answer_state not in guessed_states:

        guessed_states.append(answer_state)

        # gets row data of matching state
        state_data = data[data.state == answer_state]

        # gets coordinates from csv
        x = int(state_data.x.iloc[0])
        y = int(state_data.y.iloc[0])

        # turtle used to write state name
        writer = turtle.Turtle()

        writer.hideturtle()
        writer.penup()

        writer.goto(x, y)

        writer.write(answer_state)

screen.mainloop()