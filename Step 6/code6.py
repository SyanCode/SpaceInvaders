# -*- coding: utf-8 -*-
import turtle
import time

# Paramètres de jeu
CANNON_STEP = 10
LASER_SPEED = 1  # Réduire la vitesse du laser
ALIEN_SPEED = 0.3  # Réduire la vitesse de l'alien
ALIEN_SPAWN_INTERVAL = 1.2
DETECTION_RADIUS = 20

# Listes pour stocker les lasers et les extraterrestres
lasers = []
aliens = []
game_running = True  # Variable pour signaler la fin du jeu

# Configuration de la fenêtre
window = turtle.Screen()
window.setup(width=800, height=600)
window.bgcolor("black")
window.title("Space Invaders")
window.tracer(0)

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
    aliens.append(alien)  # Ajouter l'alien à la liste des aliens
    return alien

# Déplacer l’extraterrestre de gauche à droite et descendre à chaque changement de direction
def move_aliens():
    global ALIEN_SPEED
    for alien in aliens:
        alien.setx(alien.xcor() + ALIEN_SPEED)
        # Inverser la direction lorsque l'alien atteint les bords
        if alien.xcor() > 390 or alien.xcor() < -390:
            ALIEN_SPEED = -ALIEN_SPEED
            # Faire descendre les aliens
            for a in aliens:
                a.sety(a.ycor() - 40)  # Descendre de 40 pixels
        # Vérifier si l'alien touche le bas de l'écran
        if alien.ycor() < -300:
            global game_running
            game_running = False

# Créer un laser
def create_laser():
    laser = turtle.Turtle()
    laser.penup()
    laser.color("red")
    laser.shape("square")
    laser.shapesize(stretch_wid=0.5, stretch_len=2)
    laser.setheading(90)
    laser.setposition(cannon.xcor(), cannon.ycor() + 20)
    lasers.append(laser)  # Ajouter le laser à la liste des lasers
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

# Vérifier la collision entre un laser et l'alien
def check_collision():
    for laser in lasers[:]:
        for alien in aliens[:]:
            distance = laser.distance(alien)
            if distance < DETECTION_RADIUS:
                laser.hideturtle()
                alien.hideturtle()
                lasers.remove(laser)
                aliens.remove(alien)
                break

# Fonction pour déplacer les deux parties du canon
def move_cannon(x):
    cannon.setx(x)
    part2.setx(x)

# Déplacer le canon à gauche
def move_left():
    x = cannon.xcor() - CANNON_STEP
    if x > -390:
        move_cannon(x)

# Déplacer le canon à droite
def move_right():
    x = cannon.xcor() + CANNON_STEP
    if x < 390:
        move_cannon(x)

# Lier les touches du clavier
window.listen()
window.onkeypress(move_left, "Left")
window.onkeypress(move_right, "Right")
window.onkeypress(create_laser, "space")

# Boucle principale du jeu
alien_timer = time.time()
while game_running:
    if time.time() - alien_timer > ALIEN_SPAWN_INTERVAL:
        create_alien()
        alien_timer = time.time()
    move_aliens()  # Déplacer les extraterrestres
    move_lasers()  # Déplacer les lasers
    check_collision()  # Vérifier les collisions
    window.update()  # Mettre à jour l’écran

# Afficher "Game Over"
game_over = turtle.Turtle()
game_over.color("red")
game_over.write("GAME OVER", align="center", font=("Arial", 40, "bold"))
window.update()

# Garder la fenêtre ouverte
turtle.done()

# Questions de compréhension
# 1. On vérifie si alien.ycor() < -300 dans move_aliens().
# 2. La variable game_running contrôle si le jeu continue.
# 3. window.update() assure que "Game Over" s'affiche correctement.
# 4. Créez une fonction reset_game() pour réinitialiser les variables et relancer la boucle.
# 5. Sans pause, le jeu continuerait de s'exécuter, causant des erreurs.