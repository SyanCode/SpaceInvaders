# -*- coding: utf-8 -*-
import turtle
import time
import pygame
import json

# Initialisation de Pygame pour les sons
pygame.mixer.init()
# Charger les sons
shoot_sound = pygame.mixer.Sound(r'Step 8/tir.wav')
collision_sound = pygame.mixer.Sound(r'Step 8/collision.wav')
game_over_sound = pygame.mixer.Sound(r'Step 8/gameover.wav')

# Paramètres de jeu
CANNON_STEP = 10
LASER_SPEED = 1
ALIEN_SPEED = 0.3
ALIEN_SPAWN_INTERVAL = 1.2
DETECTION_RADIUS = 20
SCORE = 0  # Initialisation du score
LIFE = 3  # Nombre de vies
DIFFICULTY_LEVEL = 1  # Niveau de difficulté

# Listes pour stocker les lasers et les extraterrestres
lasers = []
aliens = []
game_running = True  # Variable pour signaler la fin du jeu
start_time = time.time()  # Enregistrer le temps de début du jeu

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

# Affichage du temps et du score
score_display = turtle.Turtle()
score_display.penup()
score_display.hideturtle()
score_display.setposition(350, 250)
score_display.color("white")

# Mettre à jour le score et le temps
def update_display():
    elapsed_time = time.time() - start_time
    score_display.clear()
    score_display.write(f"Temps : {elapsed_time:.1f} s\nScore : {SCORE}\nVies : {LIFE}", align="right", font=("Arial", 14, "normal"))

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
        if alien.xcor() > 390 or alien.xcor() < -390:
            ALIEN_SPEED = -ALIEN_SPEED
            for a in aliens:
                a.sety(a.ycor() - 40)
        if alien.ycor() < -300:
            global LIFE
            LIFE -= 1  # Perdre une vie si un alien atteint le bas
            if LIFE <= 0:
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
    lasers.append(laser)
    shoot_sound.play()  # Jouer le son du tir
    return laser

# Déplacer les lasers
def move_lasers():
    for laser in lasers[:]:
        laser.forward(LASER_SPEED)
        if laser.ycor() > window.window_height() / 2:
            laser.clear()
            laser.hideturtle()
            lasers.remove(laser)

# Vérifier la collision entre un laser et un extraterrestre
def check_collision():
    global SCORE
    for laser in lasers[:]:
        for alien in aliens[:]:
            distance = laser.distance(alien)
            if distance < DETECTION_RADIUS:
                laser.hideturtle()
                alien.hideturtle()
                lasers.remove(laser)
                aliens.remove(alien)
                SCORE += 10  # Incrémenter le score de 10 points
                collision_sound.play()  # Jouer le son de collision
                # Ajouter une animation d'explosion
                explosion = turtle.Turtle()
                explosion.shape("circle")
                explosion.color("yellow")
                explosion.penup()
                explosion.setposition(alien.xcor(), alien.ycor())
                explosion.shapesize(stretch_wid=1, stretch_len=1)
                explosion.showturtle()
                window.update()
                time.sleep(0.2)  # Délai pour l'effet visuel
                explosion.hideturtle()
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
    move_aliens()
    move_lasers()
    check_collision()
    update_display()  # Mettre à jour l'affichage du score et du temps
    window.update()

# Afficher "Game Over"
game_over_sound.play()  # Jouer le son de fin de partie
game_over = turtle.Turtle()
game_over.color("red")
game_over.write("GAME OVER", align="center", font=("Arial", 40, "bold"))
window.update()

# Sauvegarder le meilleur score
def save_score():
    with open("highscore.json", "w") as f:
        json.dump({"highscore": SCORE}, f)

save_score()

# Garder la fenêtre ouverte
turtle.done()
