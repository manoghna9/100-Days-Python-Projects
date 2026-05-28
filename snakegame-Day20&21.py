import tkinter 
#in-built GUI Library in python, so makes it easier to retrieve methods
import random

ROWS = 25
COLS = 25
TILE_SIZE =25
WINDOW_WIDTH = COLS * TILE_SIZE
WINDOW_HEIGHT = ROWS * TILE_SIZE

class Tile:
    def __init__(self,x,y):
        self.x=x
        self.y=y


#game window
window = tkinter.Tk()
window.title("Snake Game")
window.resizable(False, False) 
#so that user does not change size

#centering our window

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

canvas = tkinter.Canvas(window, bg = "black", width=WINDOW_WIDTH, height=WINDOW_HEIGHT, borderwidth=0,highlightthickness= 0)
canvas.pack()
window.update()

window_x=int((screen_width/2)-(WINDOW_WIDTH/2))
window_y=int((screen_height/2)-(WINDOW_HEIGHT/2))
#format is = (w)x(h)+(x)+(y)
window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{window_x}+{window_y}")

#initializing game
snake = Tile(5*TILE_SIZE,5*TILE_SIZE) #single tile, snakes head
food = Tile(10*TILE_SIZE, 10*TILE_SIZE)
snake_body =[] #multiple snake tiles
velocityX=0
velocityY=0
game_over = False
score = 0

def restart_game(): #to restart game after game over by pressing spacebar
    global snake, food, snake_body, velocityX, velocityY, game_over, score

    snake = Tile(5 * TILE_SIZE, 5 * TILE_SIZE)

    food = Tile(10 * TILE_SIZE, 10 * TILE_SIZE)

    snake_body = []
    velocityX = 0
    velocityY = 0
    score = 0
    game_over = False

def place_food():

    global food
    while True:
        food.x = random.randint(0, COLS - 1) * TILE_SIZE
        food.y = random.randint(0, ROWS - 1) * TILE_SIZE

        collision = False

        if (food.x == snake.x and food.y == snake.y):
            collision = True

        for tile in snake_body:
            if (food.x == tile.x and food.y == tile.y):
                collision = True
        if not collision:
            break


def change_direction(e): #e=event
    #print(e)
    print(e.keysym)
    global velocityX, velocityY, game_over

    if (game_over and e.keysym == "space"):
        restart_game()
        return


    if(game_over):
        return 

    if (e.keysym == "Up" and velocityY !=1):
        velocityX = 0
        velocityY = -1
    elif(e.keysym == "Down" and velocityY !=-1):
        velocityX=0
        velocityY = 1
    elif(e.keysym == "Right" and velocityX !=-1):
        velocityX = 1
        velocityY=0
    elif(e.keysym == "Left" and velocityX != 1):
        velocityX = -1
        velocityY = 0

def move():
    global snake, food, snake_body, game_over, score

    if(game_over):
        return
    if (snake.x < 0 or snake.x >=WINDOW_WIDTH or snake.y <0 or snake.y >=WINDOW_HEIGHT):
        game_over = True
        return
    for tile in snake_body: 
        if(snake.x == tile.x and snake.y == tile.y):
            game_over = True

    #collision of snake and food
    if (snake.x == food.x and snake.y == food.y):
        snake_body.append(Tile(food.x, food.y))
        place_food()
        score +=1
    
    #updating snake body
    for i in range(len(snake_body)-1, -1, -1):
        tile = snake_body[i]
        if (i==0):  
            tile.x = snake.x
            tile.y = snake.y
        else:
            prev_tile =snake_body [i-1]
            tile.x = prev_tile.x
            tile.y = prev_tile.y


    snake.x += velocityX * TILE_SIZE
    snake.y += velocityY * TILE_SIZE

def draw():
    global snake, food, snake_body, game_over, score 

    move()
    canvas.delete("all")

    #draw food
    canvas.create_rectangle(food.x, food.y, food.x+TILE_SIZE, food.y+TILE_SIZE, fill="red")

    #draw snake
    canvas.create_rectangle(snake.x, snake.y, snake.x+TILE_SIZE, snake.y + TILE_SIZE, fill="lime green")

    for tile in snake_body:
        canvas.create_rectangle(tile.x, tile.y, tile.x + TILE_SIZE, tile.y + TILE_SIZE, fill="lime green")

    if (game_over):
        canvas.create_text(WINDOW_WIDTH/2, WINDOW_HEIGHT/2, font="Arial 20", text=f"Game Over! Score: {score}\nPress SPACE to Restart", fill = "white")
    else:
        canvas.create_text(30,20, font ="Arial 10", fill = "white", text = f"Score: {score}")

    window.after(100, draw) #100 millisecods, 1/10th of a sec, calling draw every 1/10th, so 10 frames/sec

draw()

window.bind("<KeyPress>", change_direction)
window.focus_force()
window.mainloop()
