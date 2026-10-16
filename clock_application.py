import turtle
import math
from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

RADIUS = 200

THEMES = {
    "sombre": {"bg": "black", "fg": "white"},
    "clair": {"bg": "white", "fg": "black"},
}
theme = "sombre"

ZONES = [
    ("Cotonou", "Africa/Porto-Novo"),
    ("Paris", "Europe/Paris"),
    ("New York", "America/New_York"),
    ("Tokyo", "Asia/Tokyo"),
]
zone_index = 0

# Verifie que les fuseaux sont disponibles (paquet tzdata sous Windows)
try:
    TZ = [(city, ZoneInfo(name)) for city, name in ZONES]
except ZoneInfoNotFoundError:
    raise SystemExit("Fuseaux introuvables. Installe-les avec : pip install tzdata")

JOURS = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]
MOIS = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet",
        "août", "septembre", "octobre", "novembre", "décembre"]

wn = turtle.Screen()
wn.title("Analog Clock")
wn.bgcolor(THEMES[theme]["bg"])
wn.setup(500, 500)
wn.tracer(0)  # pas d'animation intermediaire -> pas de clignotement

clock = turtle.Turtle()
clock.hideturtle()

def polar(r, angle):
    """Convertit (rayon, angle en degres depuis 12h, sens horaire) en (x, y)."""
    a = math.radians(90 - angle)
    return r * math.cos(a), r * math.sin(a)

def draw_ticks(fg):
    clock.color(fg)
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

def write_text(txt, y, size, style, fg):
    clock.color(fg)
    clock.goto(0, y)
    clock.write(txt, align="center", font=("Arial", size, style))

def draw_face(fg, now, city):
    # Cercle centre sur (0, 0)
    clock.penup()
    clock.goto(0, -RADIUS)
    clock.setheading(0)
    clock.color(fg)
    clock.pensize(3)
    clock.pendown()
    clock.circle(RADIUS)
    clock.penup()

    draw_ticks(fg)

    # Chiffres 1 a 12
    for h in range(1, 13):
        x, y = polar(155, h * 30)
        clock.goto(x, y - 12)
        clock.color(fg)
        clock.write(h, align="center", font=("Arial", 16, "bold"))

    # Date, heure numerique et ville
    date_txt = f"{JOURS[now.weekday()]} {now.day} {MOIS[now.month - 1]} {now.year}"
    time_txt = f"{now.hour:02d}:{now.minute:02d}:{now.second:02d}"
    write_text(date_txt, -60, 11, "normal", fg)
    write_text(time_txt, -95, 16, "bold", fg)
    write_text(city, -122, 11, "normal", fg)

def draw_hand(angle, length, color, width):
    clock.penup()
    clock.goto(0, 0)
    clock.setheading(90 - angle)
    clock.color(color)
    clock.pensize(width)
    clock.pendown()
    clock.forward(length)
    clock.penup()

def draw():
    fg = THEMES[theme]["fg"]
    city, tz = TZ[zone_index]
    now = datetime.now(tz)
    clock.clear()
    draw_face(fg, now, city)

    sec_angle = now.second * 6
    min_angle = now.minute * 6 + now.second * 0.1
    hour_angle = (now.hour % 12) * 30 + now.minute * 0.5

    draw_hand(hour_angle, 100, "blue", 5)
    draw_hand(min_angle, 140, "green", 3)
    draw_hand(sec_angle, 160, "red", 1)

    # Point central pour cacher la jonction des aiguilles
    clock.goto(0, 0)
    clock.dot(12, fg)

    wn.update()

def update():
    draw()
    wn.ontimer(update, 1000)

def toggle_theme(x, y):
    global theme
    theme = "clair" if theme == "sombre" else "sombre"
    wn.bgcolor(THEMES[theme]["bg"])
    draw()

def next_zone():
    global zone_index
    zone_index = (zone_index + 1) % len(TZ)
    draw()

wn.onclick(toggle_theme)
wn.onkey(next_zone, "t")
wn.listen()  # indispensable pour que le clavier soit pris en compte

update()
wn.mainloop()