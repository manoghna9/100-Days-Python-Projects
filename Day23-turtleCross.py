from turtle import Turtle, Screen
import random
import time

#screensetup

screen = Screen()
screen.setup(width=600, height=600)
screen.title("Turtle Crossing")
screen.tracer(0)

#player turtle
player = Turtle()
player.shape("turtle")
player.penup()
player.goto(0, -280)
player.setheading(90)

MOVE_DISTANCE = 20

# scorecard details
level = 1
scoreboard = Turtle()
scoreboard.hideturtle()
scoreboard.penup()
scoreboard.goto(-260, 260)

def update_score(): #to update scorecard with current level
    scoreboard.clear()
    scoreboard.write(f"Level: {level}", font=("Arial", 20, "normal"))

update_score()

#car details

cars = []
car_speed = 5

colors = ["red", "orange", "yellow", "green", "blue", "purple"]

def create_car():
    random_chance = random.randint(1, 6)

    if random_chance == 1:
        car = Turtle("square")
        car.penup()
        car.shapesize(stretch_wid=1, stretch_len=2)

        car.color(random.choice(colors))

        random_y = random.randint(-250, 250)

        car.goto(300, random_y)

        cars.append(car)

def move_cars():
    for car in cars:
        car.backward(car_speed)

#moving the player turtle up on key press

def move_up():
    player.forward(MOVE_DISTANCE)

screen.listen()
screen.onkey(move_up, "Up")

#game code
game_is_on = True
while game_is_on:

    time.sleep(0.1)

    screen.update()

    create_car()
    move_cars()

    #collision with the car
    for car in cars:
        if player.distance(car) < 20:
            game_is_on = False

            game_over = Turtle()
            game_over.hideturtle()
            game_over.write( "GAME OVER", align="center", font=("Arial", 30, "bold"))

    #it reaches top
    if player.ycor() > 280:
        player.goto(0, -280)
        level += 1
        update_score()
        car_speed += 2

screen.exitonclick()