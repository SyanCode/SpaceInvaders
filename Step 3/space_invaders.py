# -*- coding: utf-8 -*-
import turtle

# Paramètres
CANNON_STEP = 10
LASER_SPEED = 15

# Configuration de la fenêtre
window = turtle.Screen()
window.setup(width=800, height=600)
window.bgcolor("black")
window.title("Space Invaders")
window.tracer(0)  # Désactiver la mise à jour automatique de l’écran

# Création du canon (partie intermédiaire)
cannon = turtle.Turtle()
cannon.penup()
cannon.color("white")
cannon.shape("square")
cannon.setposition(0, -230)
cannon.shapesize(stretch_wid=1, stretch_len=3)  # Taille moyenne

# Création de la partie supérieure du canon
def create_cannon_top():
    part2 = turtle.Turtle()
    part2.shape("square")
    part2.color("white")
    part2.penup()
    part2.speed(0)
    part2.setposition(0, -210)
    part2.shapesize(stretch_wid=1, stretch_len=1.5)  # Petite partie supérieure
    return part2

part2 = create_cannon_top()

# Déplacer le canon vers la gauche
def move_left():
    new_x = cannon.xcor() - CANNON_STEP
    if new_x >= -window.window_width() / 2 + 20:  # Garder le canon dans l’écran
        cannon.setx(new_x)
        part2.setx(new_x)  # Déplacer aussi la partie supérieure

# Déplacer le canon vers la droite
def move_right():
    new_x = cannon.xcor() + CANNON_STEP
    if new_x <= window.window_width() / 2 - 20:
        cannon.setx(new_x)
        part2.setx(new_x)  # Déplacer aussi la partie supérieure

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

# Déplacer le laser vers le haut
def move_laser(laser):
    while laser.ycor() < window.window_height() / 2:
        laser.sety(laser.ycor() + LASER_SPEED)
        window.update()  # Mettre à jour l'écran

    # Supprimer le laser lorsqu'il sort de l'écran
    laser.hideturtle()

# Tirer un laser lorsque la barre d'espace est enfoncée
def shoot_laser():
    laser = create_laser()  # Créer un nouveau laser
    move_laser(laser)  # Déplacer le laser vers le haut

# Associer les mouvements aux touches du clavier
window.listen()  # Attente des événements du clavier
window.onkeypress(move_left, "Left")  # Déplacer le canon vers la gauche
window.onkeypress(move_right, "Right")  # Déplacer le canon vers la droite
window.onkeypress(shoot_laser, "space")  # Tirer un laser lorsque la barre d'espace est enfoncée

# Boucle principale pour maintenir la fenêtre ouverte
while True:
    window.update()  # Mettre à jour l'écran
