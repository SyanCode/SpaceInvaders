# -*- coding: utf-8 -*-
import turtle

# Création de la fenêtre
window = turtle.Screen()
window.setup(width=800, height=600)
window.bgcolor("black")
window.title("Space Invaders")

# Création du canon principal
cannon = turtle.Turtle()
cannon.shape("square")
cannon.color("white")
cannon.penup()
cannon.speed(0)  # Déplacement instantané
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

# Création de la partie supérieure du canon
part2 = create_cannon_top()

# Déplacer le canon et la partie supérieure ensemble vers la gauche
def move_left():
    x = cannon.xcor()  # Position actuelle du canon
    x -= 20  # Déplacer de 20 pixels vers la gauche
    if x < -390:  # Limite de l'écran à gauche
        x = -390
    cannon.setx(x)
    part2.setx(x)  # Déplacer la partie supérieure

# Déplacer le canon et la partie supérieure ensemble vers la droite
def move_right():
    x = cannon.xcor()  # Position actuelle du canon
    x += 20  # Déplacer de 20 pixels vers la droite
    if x > 390:  # Limite de l'écran à droite
        x = 390
    cannon.setx(x)
    part2.setx(x)  # Déplacer la partie supérieure

# Associer les mouvements aux touches du clavier
window.listen()  # Attente des événements du clavier
window.onkeypress(move_left, "Left")  # Appel de la fonction move_left quand on appuie sur "Left"
window.onkeypress(move_right, "Right")  # Appel de la fonction move_right quand on appuie sur "Right"

# Garder l'écran ouvert
turtle.done()
