from turtle import Screen, Turtle
import time


screen = Screen()
screen.bgcolor("black")
screen.setup(width = 800, height = 600)
screen.title("PONG GAME")
screen.tracer(0)

class Paddle(Turtle):

    def __init__(self, position):
        super().__init__()

        self.shape("square")
        self.color("white")
        self.shapesize(stretch_wid=5, stretch_len=1)

        self.penup()
        self.goto(position)

    def go_up(self):
        new_y = self.ycor() + 20
        self.goto(self.xcor(), new_y)

    def go_down(self):
        new_y = self.ycor() - 20
        self.goto(self.xcor(), new_y)

# Ball to bounce between the paddles
ball = Turtle()
ball.shape("circle")
ball.color("white")
ball.penup()

ball.x_move = 5
ball.y_move = 5

r_paddle = Paddle((350,0))
l_paddle = Paddle((-350,0))

screen.listen()

# Right paddle
screen.onkey(r_paddle.go_up, "Up")
screen.onkey(r_paddle.go_down, "Down")

# Left paddle
screen.onkey(l_paddle.go_up, "w")
screen.onkey(l_paddle.go_down, "s")


game_is_on = True
while game_is_on:
    time.sleep(0.04) # without this, game runs TOO fast, CPU gets overloaded
    
    screen.update()
    
    # moveing the ball
    ball.goto(ball.xcor() + ball.x_move, ball.ycor() + ball.y_move)

    # when the ball hits the top or bottom wall, it should bounce
    if ball.ycor() > 280 or ball.ycor() < -280:
        ball.y_move *= -1

    # paddle collision with the ball
    if (
        ball.distance(r_paddle) < 50 and ball.xcor() > 320
    ) or (
        ball.distance(l_paddle) < 50 and ball.xcor() < -320
    ):
        ball.x_move *= -1

    # when the ball goes past the right wall, come back to centre
    if ball.xcor() > 380:
        ball.goto(0, 0)
        ball.x_move *= -1

    # when the ball goes past the left wall, come back to centre
    if ball.xcor() < -380:
        ball.goto(0, 0)
        ball.x_move *= -1

screen.exitonclick()