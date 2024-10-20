# -*- coding: utf-8 -*-
import turtle
import math

# Paramètres de jeu
CANNON_STEP = 10
LASER_SPEED = 2  # Réduire la vitesse du laser
ALIEN_SPEED = 0.3   # Réduire la vitesse de l'alien

# Configuration de la fenêtre
window = turtle.Screen()
window.setup(width=800, height=600)
window.bgcolor("black")
window.title("Space Invaders")
window.tracer(0)  # Désactiver la mise à jour automatique de l’écran

# Création du canon (partie inférieure)
cannon = turtle.Turtle()
cannon.penup()
cannon.color("white")
cannon.shape("square")
cannon.setposition(0, -230)
cannon.shapesize(stretch_wid=1, stretch_len=3)

# Création de la partie supérieure du canon
def create_cannon_top():
    part2 = turtle.Turtle()
    part2.shape("square")
    part2.color("white")
    part2.penup()
    part2.speed(0)
    part2.setposition(0, -210)
    part2.shapesize(stretch_wid=1, stretch_len=1.5)
    return part2

part2 = create_cannon_top()

# Création d’un extraterrestre
def create_alien():
    alien = turtle.Turtle()
    alien.penup()
    alien.shape("square")
    alien.color("green")
    alien.shapesize(stretch_wid=1.5, stretch_len=2)
    alien.setposition(0, 250)
    return alien

alien = create_alien()

# Déplacer l’extraterrestre de gauche à droite
def move_alien():
    global ALIEN_SPEED
    alien.setx(alien.xcor() + ALIEN_SPEED)
    # Inverser la direction lorsque l'alien atteint les bords
    if alien.xcor() > 390 or alien.xcor() < -390:
        ALIEN_SPEED = -ALIEN_SPEED

# Vérifier la collision entre un laser et l'alien
def check_collision(laser, alien):
    distance = math.sqrt(math.pow(laser.xcor() - alien.xcor(), 2) + math.pow(laser.ycor() - alien.ycor(), 2))
    return distance < 25

# Créer un laser
def create_laser():
    laser = turtle.Turtle()
    laser.penup()
    laser.color("red")
    laser.shape("square")
    laser.shapesize(stretch_wid=0.5, stretch_len=2)
    laser.setheading(90)
    laser.setposition(cannon.xcor(), cannon.ycor() + 20)
    return laser

# Déplacer les lasers
def move_lasers():
    for laser in lasers[:]:
        laser.forward(LASER_SPEED)
        # Retirer les lasers qui sortent de l’écran
        if laser.ycor() > window.window_height() / 2:
            laser.clear()
            laser.hideturtle()
            lasers.remove(laser)
        # Vérifier les collisions
        if check_collision(laser, alien):
            laser.clear()
            laser.hideturtle()
            lasers.remove(laser)
            alien.clear()
            alien.hideturtle()

# Déplacer le canon à gauche
def move_left():
    x = cannon.xcor() - CANNON_STEP
    if x > -390:  # Limite de la fenêtre
        cannon.setx(x)

# Déplacer le canon à droite
def move_right():
    x = cannon.xcor() + CANNON_STEP
    if x < 390:  # Limite de la fenêtre
        cannon.setx(x)

# Lier les touches du clavier
window.listen()
window.onkeypress(move_left, "Left")
window.onkeypress(move_right, "Right")
window.onkeypress(lambda: lasers.append(create_laser()), "space")

# Boucle de jeu principale
lasers = []

while True:
    window.update()  # Mettre à jour l’écran
    move_lasers()  # Déplacer les lasers
    move_alien()   # Déplacer l'extraterrestre de gauche à droite
    turtle.delay(10)  # Ajouter un léger délai pour la fluidité

# Garder la fenêtre ouverte
turtle.done()

# Questions de compréhension
# 1. La distance est calculée avec la formule de la distance euclidienne entre le laser et l'extraterrestre.
# 2. Sans retirer les lasers et extraterrestres après une collision, les objets restent visibles et en mémoire, perturbant le jeu.
# 3. Pas nécessaire ici, mais utile si on veut réinitialiser la position de l'extraterrestre.
# 4. Utilisation de la fonction move_alien() dans la boucle de jeu pour déplacer l'extraterrestre.
# 5. Une solution viable serait de créer une liste d'extraterrestres, parcourir cette liste, et vérifier les collisions avec chaque laser.