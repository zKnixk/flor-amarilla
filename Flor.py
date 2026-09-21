import math
import time
import turtle

ESCALA = 1.0  
PASOS_POR_FOTOGRAMA = 3  
PAUSA = 0.004            

pantalla = turtle.Screen()
pantalla.title("Tulipán amarillo")
pantalla.bgcolor("black")
pantalla.setup(int(700 * ESCALA), int(850 * ESCALA))
pantalla.tracer(0)  

t = turtle.Turtle()
t.hideturtle()
t.speed(0)

pasos_dados = 0
animar = False

def avanzar(x, y):
    global pasos_dados
    t.goto(x * ESCALA, y * ESCALA)
    pasos_dados += 1
    if animar and pasos_dados % PASOS_POR_FOTOGRAMA == 0:
        pantalla.update()
        time.sleep(PAUSA)


def ir_a(x, y):
    t.penup()
    t.goto(x * ESCALA, y * ESCALA)
    t.pendown()


def punto(p0, p1, p2, p3, s):
    a = (1 - s) ** 3
    b = 3 * (1 - s) ** 2 * s
    c = 3 * (1 - s) * s ** 2
    d = s ** 3
    return (a * p0[0] + b * p1[0] + c * p2[0] + d * p3[0],
            a * p0[1] + b * p1[1] + c * p2[1] + d * p3[1])


def mezcla(a, b, f):
    return (a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f)


def curva(p0, p1, p2, p3, pasos=40):
    for i in range(1, pasos + 1):
        avanzar(*punto(p0, p1, p2, p3, i / pasos))


def trazo(p0, p1, p2, p3, color, grosor, pasos=40):
    ir_a(*p0)
    t.color(color)
    t.pensize(grosor * ESCALA)
    curva(p0, p1, p2, p3, pasos)


def recta(a, b, color, grosor):
    ir_a(*a)
    t.color(color)
    t.pensize(grosor * ESCALA)
    avanzar(*b)


def forma(inicio, curvas, relleno, borde, grosor=3, pasos=40):
    ir_a(*inicio)
    t.color(borde, relleno)
    t.pensize(grosor * ESCALA)
    t.begin_fill()
    p = inicio
    for c1, c2, fin in curvas:
        curva(p, c1, c2, fin, pasos)
        p = fin
    t.end_fill()


def disco(cx, cy, r, color, lados=48):
    ir_a(cx + r, cy)
    t.color(color)
    t.pensize(1)
    t.begin_fill()
    for i in range(1, lados + 1):
        a = 2 * math.pi * i / lados
        avanzar(cx + r * math.cos(a), cy + r * math.sin(a))
    t.end_fill()


def escalar(inicio, curvas, k, centro):
    cx, cy = centro

    def f(p):
        return (cx + (p[0] - cx) * k, cy + (p[1] - cy) * k)

    return f(inicio), [(f(a), f(b), f(c)) for a, b, c in curvas]


def petalo(inicio, curvas, base, borde, capas, centro):
    forma(inicio, curvas, base, borde)
    for k, color in capas:
        ini, cur = escalar(inicio, curvas, k, centro)
        forma(ini, cur, color, color, grosor=1, pasos=25)


def hoja(lado, tx, ty, gota=None):
    S, T = (lado * 6, -395), (tx, ty)
    c1o, c2o = (lado * 130, -395), (tx + lado * 25, ty - 165)
    c1i, c2i = (tx - lado * 40, ty - 145), (lado * 70, -330)
    m1 = mezcla(c1o, c2i, 0.5)
    m2 = mezcla(c2o, c1i, 0.5)

    forma(S, [(c1o, c2o, T), (c1i, c2i, S)], "#39b25c", "#1f7a3a")
    forma(S, [(c1o, c2o, T), (m2, m1, S)], "#2a9a4c", "#1f7a3a", grosor=1)
    trazo(S, m1, m2, T, "#8be6a0", 2)

    for s in (0.18, 0.30, 0.42, 0.54, 0.66, 0.78):
        centro = punto(S, m1, m2, T, s)
        for borde in (punto(S, c1o, c2o, T, s + 0.09),
                      punto(S, c2i, c1i, T, s + 0.09)):
            recta(centro, mezcla(centro, borde, 0.8), "#6fd08a", 1.5)

    if gota is not None:
        x, y = punto(S, m1, m2, T, gota)
        disco(x, y, 8, "#8fd8f5", 20)
        disco(x - 2.5, y + 2.5, 3, "white", 12)

for i in range(8):
    f = i / 7
    color = "#%02x%02x%02x" % (7 + int(35 * f), 5 + int(28 * f), 0)
    disco(0, 150, 270 - 20 * i, color, lados=60)
pantalla.update()
animar = True

tallo = [(0, -400), (-35, -260), (35, -130), (0, 20)]
trazo(*tallo, "#3aa655", 12, pasos=60)
trazo(*[(x - 2.5, y) for x, y in tallo], "#7be08f", 2.5, pasos=60)
trazo(*[(x + 3.5, y) for x, y in tallo], "#237a3c", 2.5, pasos=60)

hoja(-1, -190, -95)
hoja(1, 175, -150, gota=0.55)

forma((0, 0),
      [((-130, 40), (-125, 230), (0, 335)),
       ((125, 230), (130, 40), (0, 0))],
      "#c98600", "#94670a", pasos=50)

for lado in (-1, 1):
    petalo((0, 0),
           [((lado * 170, 20), (lado * 160, 200), (lado * 95, 295)),
            ((lado * 20, 240), (lado * 10, 120), (0, 0))],
           "#dc9a00", "#a87400",
           [(0.88, "#eaa900"), (0.68, "#f4bb10"), (0.46, "#fcd02e")],
           (lado * 80, 160))
    trazo((0, 8), (lado * 140, 40), (lado * 140, 190), (lado * 92, 282), "#b97f00", 1.5)
    trazo((0, 8), (lado * 100, 50), (lado * 100, 200), (lado * 78, 270), "#b97f00", 1.5)

petalo((0, 0),
       [((-110, 60), (-90, 200), (0, 310)),
        ((90, 200), (110, 60), (0, 0))],
       "#f5bd00", "#c99700",
       [(0.86, "#ffd000"), (0.66, "#ffdc2e"), (0.44, "#ffe766"), (0.24, "#fff09a")],
       (0, 165))
for o in (-46, -24, 0, 24, 46):  # venas que se abren desde la base
    trazo((0, 14), (o * 1.6, 90), (o * 1.3, 210), (o * 0.2, 292), "#e0a700", 1.5)

forma((-40, 110),
      [((-52, 150), (-44, 200), (-24, 238)),
       ((-34, 200), (-34, 150), (-40, 110))],
      "#fff6b0", "#fff6b0", grosor=1, pasos=25)

forma((-22, 12),
      [((-30, -20), (30, -20), (22, 12)),
       ((10, 2), (-10, 2), (-22, 12))],
      "#3aa655", "#237a3c", pasos=30)

pantalla.update()
pantalla.exitonclick()
