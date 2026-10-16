import turtle
import time
import math

wn = turtle.Screen()
wn.title("Analog Clock")
wn.bgcolor("black")
wn.setup(500, 500)
wn.tracer(0)  # pas d'animation intermédiaire -> pas de clignotement

clock = turtle.Turtle()
clock.hideturtle()

def draw_face():
    # Cercle centré sur (0, 0)
    clock.penup()
    clock.goto(0, -200)
    clock.setheading(0)
    clock.color("white")
    clock.pensize(3)
    clock.pendown()
    clock.circle(200)

    # Chiffres 1 à 12
    clock.penup()
    for h in range(1, 13):
        a = math.radians(90 - h * 30)
        x = 170 * math.cos(a)
        y = 170 * math.sin(a)
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

    wn.update()
    wn.ontimer(update, 1000)  # relance dans 1 seconde

update()
wn.mainloop()