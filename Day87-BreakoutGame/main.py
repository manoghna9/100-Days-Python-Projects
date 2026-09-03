"""
Original Breakout implementation using Python Turtle.

Controls:
    Left / Right arrows -> move the paddle
    Space -> launch the ball
    R -> restart the game
    Esc -> quit

The game is intentionally split into small classes so that each object
has one clear responsibility:
    Paddle -> player movement
    Ball   -> movement and collision detection
    Brick  -> individual blocks
    Game   -> score, lives and overall game state
"""

from turtle import Screen, Turtle
import random
import time


# -----------------------------
# Game configuration
# -----------------------------
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 700

PADDLE_WIDTH = 120
PADDLE_Y = -300

BALL_SIZE = 18

BRICK_WIDTH = 78
BRICK_HEIGHT = 24
BRICK_GAP = 8

BRICK_ROWS = 7
BRICK_COLUMNS = 10

START_LIVES = 3


class Paddle(Turtle):
    """The blue paddle controlled by the player."""

    def __init__(self):
        super().__init__()
        self.shape("square")
        self.color("deepskyblue")
        self.shapesize(stretch_wid=0.55, stretch_len=PADDLE_WIDTH / 20)
        self.penup()
        self.goto(0, PADDLE_Y)
        self.dx = 0

    def move_left(self):
        """Move left, but do not leave the screen."""
        self.setx(max(-SCREEN_WIDTH / 2 + 70, self.xcor() - 35))

    def move_right(self):
        """Move right, but do not leave the screen."""
        self.setx(min(SCREEN_WIDTH / 2 - 70, self.xcor() + 35))


class Ball(Turtle):
    """The ball. It remembers its x/y movement separately."""

    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.color("white")
        self.shapesize(BALL_SIZE / 20)
        self.penup()
        self.reset()

    def reset(self):
        """Put the ball back on the paddle."""
        self.goto(0, PADDLE_Y + 25)
        self.dx = 0
        self.dy = 0
        self.launched = False

    def launch(self):
        """Start the ball with a slightly random horizontal direction."""
        if not self.launched:
            self.dx = random.choice([-5, -4, 4, 5])
            self.dy = 5
            self.launched = True

    def move(self):
        """Move the ball by its current velocity."""
        self.goto(self.xcor() + self.dx, self.ycor() + self.dy)


class Brick(Turtle):
    """One breakable brick."""

    COLORS = [
        "red",
        "orange",
        "gold",
        "green",
        "cyan",
        "dodgerblue",
        "purple",
    ]

    def __init__(self, x, y, row):
        super().__init__()
        self.shape("square")
        self.color(self.COLORS[row])
        self.shapesize(
            stretch_wid=BRICK_HEIGHT / 20,
            stretch_len=BRICK_WIDTH / 20,
        )
        self.penup()
        self.goto(x, y)
        self.points = BRICK_ROWS - row

    def destroy(self):
        """Hide this brick and remove its turtle from the game."""
        self.hideturtle()


class Scoreboard:
    """Draws the score and lives at the top of the screen."""

    def __init__(self):
        self.writer = Turtle(visible=False)
        self.writer.color("white")
        self.writer.penup()
        self.writer.goto(0, 315)
        self.score = 0
        self.lives = START_LIVES
        self.update()

    def update(self):
        self.writer.clear()
        self.writer.write(
            f"Score: {self.score}     Lives: {self.lives}",
            align="center",
            font=("Arial", 20, "bold"),
        )

    def add_points(self, amount):
        self.score += amount
        self.update()

    def lose_life(self):
        self.lives -= 1
        self.update()


class Game:
    """Coordinates all the objects and contains the main game loop."""

    def __init__(self):
        self.screen = Screen()
        self.screen.setup(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.screen.bgcolor("black")
        self.screen.title("Breakout - Original Implementation")
        self.screen.tracer(0)

        self.paddle = Paddle()
        self.ball = Ball()
        self.scoreboard = Scoreboard()
        self.bricks = []

        self.running = True
        self.waiting_for_launch = True

        self.create_bricks()
        self.bind_controls()

    def create_bricks(self):
        """Create a centered grid of bricks."""
        total_width = (
            BRICK_COLUMNS * BRICK_WIDTH
            + (BRICK_COLUMNS - 1) * BRICK_GAP
        )
        start_x = -total_width / 2 + BRICK_WIDTH / 2

        start_y = 250

        for row in range(BRICK_ROWS):
            for column in range(BRICK_COLUMNS):
                x = start_x + column * (BRICK_WIDTH + BRICK_GAP)
                y = start_y - row * (BRICK_HEIGHT + BRICK_GAP)

                self.bricks.append(Brick(x, y, row))

    def bind_controls(self):
        """Connect keyboard keys to paddle/game actions."""
        self.screen.listen()
        self.screen.onkeypress(self.paddle.move_left, "Left")
        self.screen.onkeypress(self.paddle.move_right, "Right")
        self.screen.onkeypress(self.ball.launch, "space")
        self.screen.onkeypress(self.restart, "r")
        self.screen.onkeypress(self.restart, "R")
        self.screen.onkeypress(self.quit_game, "Escape")

    def wall_collision(self):
        """Bounce the ball from the left, right and top walls."""
        if self.ball.xcor() >= SCREEN_WIDTH / 2 - 15:
            self.ball.setx(SCREEN_WIDTH / 2 - 15)
            self.ball.dx *= -1

        if self.ball.xcor() <= -SCREEN_WIDTH / 2 + 15:
            self.ball.setx(-SCREEN_WIDTH / 2 + 15)
            self.ball.dx *= -1

        if self.ball.ycor() >= SCREEN_HEIGHT / 2 - 15:
            self.ball.sety(SCREEN_HEIGHT / 2 - 15)
            self.ball.dy *= -1

    def paddle_collision(self):
        """Bounce the ball when it reaches the paddle."""
        if (
            self.ball.dy < 0
            and PADDLE_Y - 15 < self.ball.ycor() < PADDLE_Y + 25
            and abs(self.ball.xcor() - self.paddle.xcor()) < 75
        ):
            self.ball.sety(PADDLE_Y + 25)
            self.ball.dy = abs(self.ball.dy)

            # The hit position changes the horizontal direction.
            offset = self.ball.xcor() - self.paddle.xcor()
            self.ball.dx = max(-7, min(7, offset / 10))

            # Prevent a perfectly vertical trajectory.
            if abs(self.ball.dx) < 1.5:
                self.ball.dx = random.choice([-2.5, 2.5])

    def brick_collision(self):
        """Check whether the ball has hit any visible brick."""
        for brick in self.bricks:
            if not brick.isvisible():
                continue

            horizontal_hit = abs(self.ball.xcor() - brick.xcor()) < 48
            vertical_hit = abs(self.ball.ycor() - brick.ycor()) < 20

            if horizontal_hit and vertical_hit:
                # We only need one brick per frame.
                brick.destroy()
                self.scoreboard.add_points(brick.points)

                # Reverse the vertical direction for a simple,
                # predictable Breakout-style collision.
                self.ball.dy *= -1
                return

    def ball_fell(self):
        """Handle the ball passing below the paddle."""
        if self.ball.ycor() < -SCREEN_HEIGHT / 2:
            self.scoreboard.lose_life()

            if self.scoreboard.lives <= 0:
                self.end_game("GAME OVER")
            else:
                self.ball.reset()

    def all_bricks_gone(self):
        """Return True when every brick has been destroyed."""
        return all(not brick.isvisible() for brick in self.bricks)

    def show_message(self, message):
        writer = Turtle(visible=False)
        writer.color("white")
        writer.penup()
        writer.goto(0, -20)
        writer.write(
            message,
            align="center",
            font=("Arial", 32, "bold"),
        )
        self.screen.update()

    def end_game(self, message):
        self.running = False
        self.ball.reset()
        self.show_message(message + "\nPress R to play again")

    def restart(self):
        """Reset the entire game."""
        for brick in self.bricks:
            brick.hideturtle()

        self.bricks.clear()
        self.paddle.goto(0, PADDLE_Y)
        self.scoreboard.score = 0
        self.scoreboard.lives = START_LIVES
        self.scoreboard.update()

        self.running = True
        self.create_bricks()
        self.ball.reset()

        # Remove any old message writers by clearing the screen's
        # drawing layer is avoided; the new game simply starts cleanly.
        self.screen.update()

    def quit_game(self):
        self.screen.bye()

    def run(self):
        """Main game loop."""
        while True:
            if self.running and self.ball.launched:
                self.ball.move()
                self.wall_collision()
                self.paddle_collision()
                self.brick_collision()
                self.ball_fell()

                if self.all_bricks_gone() and self.running:
                    self.end_game("YOU WIN!")

            self.screen.update()
            time.sleep(0.01)


if __name__ == "__main__":
    game = Game()
    game.run()
