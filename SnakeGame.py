import turtle
import random
import tkinter as tk
from tkinter import messagebox

# Constants
WIDTH = 1500
HEIGHT = 700
FOOD_SIZE = 10
DELAY = 100
offsets = {
    "up": (0, 20),
    "down": (0, -20),
    "left": (-20, 0),
    "right": (20, 0)
}

# Global variables
high_score = 0

def reset():
    global snake, snake_direction, food_pos, pen, score
    score = 0
    snake = [[0, 0], [0, 20], [0, 40], [0, 50], [0, 60]]
    snake_direction = "up"
    food_pos = get_random_food_pos()
    food.goto(food_pos)
    move_snake()

def move_snake():
    global snake_direction, score

    # Next position for head of snake.
    new_head = snake[-1].copy()
    new_head[0] = snake[-1][0] + offsets[snake_direction][0]
    new_head[1] = snake[-1][1] + offsets[snake_direction][1]

    # Check self-collision
    if new_head in snake[:-1]:
        check_high_score()
        return

    snake.append(new_head)
    if not food_collision():
        snake.pop(0)  # Keep the snake the same length unless fed.

    # Check screen collision
    if abs(snake[-1][0]) > WIDTH / 2 or abs(snake[-1][1]) > HEIGHT / 2:
        check_high_score()
        return

    # Allow screen wrapping
    if snake[-1][0] > WIDTH / 2:
        snake[-1][0] -= WIDTH
    elif snake[-1][0] < - WIDTH / 2:
        snake[-1][0] += WIDTH
    elif snake[-1][1] > HEIGHT / 2:
        snake[-1][1] -= HEIGHT
    elif snake[-1][1] < -HEIGHT / 2:
        snake[-1][1] += HEIGHT

    # Clear previous snake stamps
    pen.clearstamps()

    # Draw snake
    for segment in snake:
        pen.goto(segment[0], segment[1])
        pen.stamp()

    # Refresh screen
    screen.update()

    # Rinse and repeat
    turtle.ontimer(move_snake, DELAY)

def food_collision():
    global food_pos, score
    if get_distance(snake[-1], food_pos) < 20:
        food_pos = get_random_food_pos()
        food.goto(food_pos)
        score += 1
        return True
    return False

def get_random_food_pos():
    x = random.randint(int(- WIDTH / 2 + FOOD_SIZE), int(WIDTH / 2 - FOOD_SIZE))
    y = random.randint(int(- HEIGHT / 2 + FOOD_SIZE), int(HEIGHT / 2 - FOOD_SIZE))
    return (x, y)

def get_distance(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    distance = ((y2 - y1) ** 2 + (x2 - x1) ** 2) ** 0.5
    return distance

def go_up():
    global snake_direction
    if snake_direction != "down":
        snake_direction = "up"

def go_right():
    global snake_direction
    if snake_direction != "left":
        snake_direction = "right"

def go_down():
    global snake_direction
    if snake_direction != "up":
        snake_direction = "down"

def go_left():
    global snake_direction
    if snake_direction != "right":
        snake_direction = "left"

def check_high_score():
    global score, high_score
    if score > high_score:
        high_score = score
        messagebox.showinfo("Game Over", f"New High Score! Your score is {score}")
    else:
        messagebox.showinfo("Game Over", f"Your score is {score}")

    ask_to_play_again()

def ask_to_play_again():
    global root
    top = tk.Toplevel(root)
    top.title("Play Again?")
    top.geometry("300x150+{}+{}".format(root.winfo_x(), root.winfo_y()))

    msg = tk.Label(top, text="Do you want to play again?")
    msg.pack(pady=10)

    play_again_button = tk.Button(top, text="Play Again", command=lambda: [top.destroy(), reset()])
    play_again_button.pack(pady=10)

    close_button = tk.Button(top, text="Close Game", command=close_game)
    close_button.pack(pady=10)

def start_game():
    global root
    root.withdraw()  # Hide the root window instead of destroying it
    screen_setup()
    reset()
    turtle.done()

def close_game():
    global root
    try:
        root.destroy()
    except:
        pass
    turtle.bye()

def screen_setup():
    global screen, pen, food
    # Screen
    screen = turtle.Screen()
    screen.setup(WIDTH, HEIGHT)
    screen.title("Snake Game")
    screen.bgcolor("black")
    screen.setup(1500, 700)
    screen.tracer(0)

    # Pen
    pen = turtle.Turtle("square")
    pen.penup()
    pen.pencolor("yellow")

    # Food
    food = turtle.Turtle()
    food.shape("circle")
    food.color("red")
    food.shapesize(FOOD_SIZE / 20)  # Default size of turtle "square" shape is 20.
    food.penup()

    # Event handlers
    screen.listen()
    screen.onkey(go_up, "Up")
    screen.onkey(go_right, "Right")
    screen.onkey(go_down, "Down")
    screen.onkey(go_left, "Left")

# Create start menu
root = tk.Tk()
root.geometry("250x100+600+360")
root.title("Snake Game")

start_button = tk.Button(root, text="Start Game", command=start_game)
start_button.pack(pady=10)

close_button = tk.Button(root, text="Close Game", command=close_game)
close_button.pack(pady=10)

root.mainloop()
