import turtle

# Setup the window
window = turtle.Screen()
window.title("Pong Game By @MittalGmt")
window.bgcolor("black")
window.setup(width=800, height=600)
window.tracer(0)

# Paddle A
paddle_a = turtle.Turtle()
paddle_a.speed(0)
paddle_a.shape("square")
paddle_a.color("white")
paddle_a.shapesize(stretch_wid=5, stretch_len=1)
paddle_a.penup()
paddle_a.goto(-350, 0)

# Paddle B
paddle_b = turtle.Turtle()
paddle_b.speed(0)
paddle_b.shape("square")
paddle_b.color("white")
paddle_b.shapesize(stretch_wid=5, stretch_len=1)
paddle_b.penup()
paddle_b.goto(350, 0)

# Ball
ball = turtle.Turtle()
ball.speed(0)
ball.shape("circle")
ball.color("white")
ball.penup()
ball.goto(0, 0)
ball.dx = 0.1  
ball.dy = 0.1  

# Score variables
score_a = 0
score_b = 0

# Scoreboard
scoreboard = turtle.Turtle()
scoreboard.speed(0)
scoreboard.color("white")
scoreboard.penup()
scoreboard.hideturtle()
scoreboard.goto(0, 260)
scoreboard.write("Player A: 0  Player B: 0", align="center", font=("Courier", 24, "normal"))

# Function to update the scoreboard
def update_scoreboard():
    scoreboard.clear()
    scoreboard.write(f"Player A: {score_a}  Player B: {score_b}", align="center", font=("Courier", 24, "normal"))

# Function to move paddle A up
def paddle_a_up():
    y = paddle_a.ycor()
    if y < 250:  
        y += 20
    paddle_a.sety(y)

# Function to move paddle A down
def paddle_a_down():
    y = paddle_a.ycor()
    if y > -240:  
        y -= 20
    paddle_a.sety(y)

# Function to move paddle B up
def paddle_b_up():
    y = paddle_b.ycor()
    if y < 250:
        y += 20
    paddle_b.sety(y)

# Function to move paddle B down
def paddle_b_down():
    y = paddle_b.ycor()
    if y > -240:  
        y -= 20
    paddle_b.sety(y)

# Keyboard bindings
window.listen()
window.onkeypress(paddle_a_up, "w")
window.onkeypress(paddle_a_down, "s")
window.onkeypress(paddle_b_up, "Up")
window.onkeypress(paddle_b_down, "Down")

# Main game loop
while True:
    try:
        window.update()
        
        # Move the ball
        ball.setx(ball.xcor() + ball.dx)
        ball.sety(ball.ycor() + ball.dy)
        
        # Border checking
        if ball.ycor() > 290:
            ball.sety(290)
            ball.dy *= -1
        
        if ball.ycor() < -290:
            ball.sety(-290)
            ball.dy *= -1
        
        if ball.xcor() > 390:
            ball.goto(0, 0)
            ball.dx *= -1
            score_a += 1
            update_scoreboard()
        
        if ball.xcor() < -390:
            ball.goto(0, 0)
            ball.dx *= -1
            score_b += 1
            update_scoreboard()
        
        # Paddle and ball collision
        if (ball.dx > 0 and 340 < ball.xcor() < 350) and (paddle_b.ycor() - 50 < ball.ycor() < paddle_b.ycor() + 50):
            ball.setx(340)
            ball.dx *= -1
        
        if (ball.dx < 0 and -350 < ball.xcor() < -340) and (paddle_a.ycor() - 50 < ball.ycor() < paddle_a.ycor() + 50):
            ball.setx(-340)
            ball.dx *= -1

    except turtle.Terminator:
        break  
