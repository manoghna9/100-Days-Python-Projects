import turtle
import random
import time


# ==========================================================
# GAME SETTINGS
# ==========================================================

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700

PLAYER_SPEED = 25
BULLET_SPEED = 15

ALIEN_HORIZONTAL_SPEED = 2
ALIEN_DROP_DISTANCE = 25

GAME_RUNNING = True
ALIEN_DIRECTION = 1

score = 0


# ==========================================================
# CREATE THE SCREEN
# ==========================================================

screen = turtle.Screen()

screen.setup(
    width=SCREEN_WIDTH,
    height=SCREEN_HEIGHT
)

screen.bgcolor("black")
screen.title("Space Invaders")

screen.tracer(0)


# ==========================================================
# PLAYER
# ==========================================================

player = turtle.Turtle()

player.shape("triangle")
player.color("white")

player.penup()

player.setheading(90)

player.goto(
    0,
    -300
)


# ==========================================================
# PLAYER MOVEMENT
# ==========================================================

def move_left():

    x = player.xcor()

    if x > -370:

        player.setx(
            x - PLAYER_SPEED
        )


def move_right():

    x = player.xcor()

    if x < 370:

        player.setx(
            x + PLAYER_SPEED
        )


# Keyboard controls

screen.listen()

screen.onkeypress(
    move_left,
    "Left"
)

screen.onkeypress(
    move_right,
    "Right"
)


# ==========================================================
# BULLET
# ==========================================================

bullet = turtle.Turtle()

bullet.shape("square")
bullet.color("yellow")

bullet.shapesize(
    stretch_wid=0.2,
    stretch_len=0.8
)

bullet.penup()

bullet.hideturtle()

bullet.setheading(90)

bullet_active = False


# ==========================================================
# SHOOT
# ==========================================================

def shoot():

    global bullet_active

    # Don't allow another bullet while
    # the current one is still on screen.
    if not bullet_active:

        bullet_active = True

        bullet.goto(
            player.xcor(),
            player.ycor() + 15
        )

        bullet.showturtle()


screen.onkeypress(
    shoot,
    "space"
)


# ==========================================================
# ALIENS
# ==========================================================

aliens = []


def create_aliens():

    for row in range(4):

        for column in range(8):

            alien = turtle.Turtle()

            alien.shape("turtle")

            alien.color(
                random.choice(
                    ["red", "green", "purple"]
                )
            )

            alien.penup()

            x = -280 + column * 80

            y = 230 - row * 55

            alien.goto(x, y)

            aliens.append(alien)


create_aliens()


# ==========================================================
# BARRIERS
# ==========================================================

barriers = []


def create_barriers():

    barrier_positions = [
        -270,
        -90,
        90,
        270
    ]

    for x_position in barrier_positions:

        barrier = turtle.Turtle()

        barrier.shape("square")

        barrier.color("cyan")

        barrier.shapesize(
            stretch_wid=1.5,
            stretch_len=4
        )

        barrier.penup()

        barrier.goto(
            x_position,
            -200
        )

        barriers.append(barrier)


create_barriers()


# ==========================================================
# SCORE DISPLAY
# ==========================================================

score_writer = turtle.Turtle()

score_writer.color("white")

score_writer.penup()

score_writer.hideturtle()

score_writer.goto(
    -360,
    310
)


def update_score():

    score_writer.clear()

    score_writer.write(
        f"Score: {score}",
        font=(
            "Arial",
            16,
            "normal"
        )
    )


update_score()


# ==========================================================
# GAME OVER DISPLAY
# ==========================================================

game_over_writer = turtle.Turtle()

game_over_writer.color("red")

game_over_writer.penup()

game_over_writer.hideturtle()

game_over_writer.goto(
    0,
    0
)


def game_over():

    global GAME_RUNNING

    GAME_RUNNING = False

    game_over_writer.write(
        "GAME OVER",
        align="center",
        font=(
            "Arial",
            40,
            "bold"
        )
    )


# ==========================================================
# COLLISION FUNCTION
# ==========================================================

def is_collision(object_one, object_two):

    distance = object_one.distance(
        object_two
    )

    return distance < 25


# ==========================================================
# MAIN GAME LOOP
# ==========================================================

while GAME_RUNNING:

    # ------------------------------------------------------
    # MOVE BULLET
    # ------------------------------------------------------

    if bullet_active:

        bullet.sety(
            bullet.ycor() + BULLET_SPEED
        )

        # Bullet left the screen
        if bullet.ycor() > 330:

            bullet.hideturtle()

            bullet_active = False


    # ------------------------------------------------------
    # CHECK BULLET AGAINST ALIENS
    # ------------------------------------------------------

    if bullet_active:

        for alien in aliens:

            if is_collision(
                bullet,
                alien
            ):

                # Remove the alien
                alien.hideturtle()

                aliens.remove(
                    alien
                )

                # Remove the bullet
                bullet.hideturtle()

                bullet_active = False

                # Increase score
                score += 10

                update_score()

                break


    # ------------------------------------------------------
    # MOVE ALIENS
    # ------------------------------------------------------

    edge_reached = False

    for alien in aliens:

        alien.setx(
            alien.xcor()
            + ALIEN_HORIZONTAL_SPEED
            * ALIEN_DIRECTION
        )

        # Check whether an alien reached
        # either side of the screen.
        if alien.xcor() > 360 or alien.xcor() < -360:

            edge_reached = True


    # ------------------------------------------------------
    # DROP ALIENS WHEN THEY HIT AN EDGE
    # ------------------------------------------------------

    if edge_reached:

        ALIEN_DIRECTION *= -1

        for alien in aliens:

            alien.sety(
                alien.ycor()
                - ALIEN_DROP_DISTANCE
            )


    # ------------------------------------------------------
    # CHECK WHETHER ALIENS REACHED PLAYER
    # ------------------------------------------------------

    for alien in aliens:

        if alien.ycor() < -250:

            game_over()

            break

    # ------------------------------------------------------
    # CHECK WHETHER ALIENS HIT BARRIERS
    # ------------------------------------------------------

    for alien in aliens:

        for barrier in barriers:

            if is_collision(
                alien,
                barrier
            ):

                barrier.hideturtle()

                barriers.remove(
                    barrier
                )

                break


    # ------------------------------------------------------
    # CHECK WHETHER BULLET HIT BARRIER
    # ------------------------------------------------------

    if bullet_active:

        for barrier in barriers:

            if is_collision(
                bullet,
                barrier
            ):

                bullet.hideturtle()

                bullet_active = False

                break


    # ------------------------------------------------------
    # UPDATE SCREEN
    # ------------------------------------------------------

    screen.update()

    time.sleep(0.02)


# ==========================================================
# KEEP WINDOW OPEN AFTER GAME OVER
# ==========================================================

screen.mainloop()