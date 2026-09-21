import turtle

pantalla = turtle.Screen()
pantalla.title("Flor Amarilla")
pantalla.bgcolor("#e8f6ff")

t = turtle.Turtle()
t.hideturtle()

CENTRO_Y = 100

def ir_a(x, y):
    t.penup
    t.goto(x, y)
    t.pendown()

def hoja(x, y, angulo, radio, relleno, borde, apertura=60):
    ir_a(x, y)
    t.setheading(angulo)
    t.color(borde, relleno)
    t.begin_fill()
    t.circle(radio, apertura)
    t.left(180 - apertura)
    t.circle(radio, apertura)
    t.end_fill()

t.speed(3)
t.pensize(8)
t.color("forestgreen")
ir_a(0, -300)
t.setheading(90)
t.forward(CENTRO_Y + 300)

t.pensize(2)
hoja(0, -200, 15, 60, "limegreen", "forestgreen")
hoja(0, -120, 105, 60, "limegreen", "forestgreen")

t.speed(6)
for angulo in range(-135, 225, 30):
    hoja(0, CENTRO_Y, angulo, 50, "gold", "goldenrod", apertura=90)

t.color("saddlebrown", "saddlebrown")
ir_a(0, CENTRO_Y - 25)
t.setheading(0)
t.begin_fill()
t.circle(25)
t.end_fill

pantalla.exitonclick()