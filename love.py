import turtle

screen = turtle.Screen()
screen.bgcolor("black")
screen.title("Te quiero Kam <3")

pen = turtle.Turtle()
pen.hideturtle()
pen.speed(5)
pen.color("red")

pen.begin_fill()
pen.left(50)
pen.forward(133)
pen.circle(50, 200)
pen.right(140)
pen.circle(50, 200)
pen.forward(133)
pen.end_fill()

pen.penup()
pen.goto(0, -180)
pen.color("white")
pen.write("Te quiero Kam <3", align="center", font=("Arial", 24, "bold"))

turtle.done()
