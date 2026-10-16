import turtle
import time
import math

RADIUS = 200

wn = turtle.Screen()
wn.title("Analog Clock")
wn.bgcolor("black")
wn.setup(500, 500)
wn.tracer(0)  # pas d'animation intermédiaire -> pas de clignotement

clock = turtle.Turtle()
clock.hideturtle()

def polar(r, angle):
    """Convertit (rayon, angle en degrés depuis 12h, sens horaire) en (x, y)."""
    a = math.radians(90 - angle)
    return r * math.cos(a), r * math.sin(a)

def draw_ticks():
    clock.color("white")
    for i in range(60):
        angle = i * 6
        is_hour = i % 5 == 0
        length = 15 if is_hour else 6
        clock.pensize(3 if is_hour else 1)
        x1, y1 = polar(RADIUS - length, angle)
        x2, y2 = polar(RADIUS, angle)
        clock.penup()
        clock.goto(x1, y1)
        clock.pendown()
        clock.goto(x2, y2)
    clock.penup()

def draw_face():
    # Cercle centré sur (0, 0)
    clock.penup()
    clock.goto(0, -RADIUS)
    clock.setheading(0)
    clock.color("white")
    clock.pensize(3)
    clock.pendown()
    clock.circle(RADIUS)
    clock.penup()

    draw_ticks()

    # Chiffres 1 à 12
    clock.color("white")
    for h in range(1, 13):
        x, y = polar(155, h * 30)
        clock.goto(x, y - 12)  # -12 pour centrer verticalement le texte
        clock.write(h, align="center", font=("Arial", 16, "bold"))

def draw_hand(angle, length, color, width):
    clock.penup()
    clock.goto(0, 0)
    clock.setheading(90 - angle)
    clock.color(color)
    clock.pensize(width)
    clock.pendown()
    clock.forward(length)
    clock.penup()

def update():
    clock.clear()
    draw_face()

    now = time.localtime()
    sec = now.tm_sec
    min_ = now.tm_min
    hour = now.tm_hour % 12

    sec_angle = sec * 6
    min_angle = min_ * 6 + sec * 0.1
    hour_angle = hour * 30 + min_ * 0.5

    draw_hand(hour_angle, 100, "blue", 5)
    draw_hand(min_angle, 140, "green", 3)
    draw_hand(sec_angle, 160, "red", 1)

    # Point central pour cacher la jonction des aiguilles
    clock.goto(0, 0)
    clock.dot(12, "white")

    wn.update()
    wn.ontimer(update, 1000)

update()
wn.mainloop() 