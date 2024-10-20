import turtle
import time
import pygame
import json
from pymongo import MongoClient

# Initialisation de Pygame pour les sons
pygame.mixer.init()
shoot_sound = pygame.mixer.Sound(r'final/tir.wav')
collision_sound = pygame.mixer.Sound(r'final/collision.wav')
game_over_sound = pygame.mixer.Sound(r'final/gameover.wav')

# Initialisation de MongoDB
client = MongoClient('mongodb+srv://spaceInvaders:<miaou>@cluster0.3p47e.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client['space_invaders']  # Nom de la base de données
scores_collection = db['scores']  # Nom de la collection pour stocker les scores

# Paramètres de jeu par défaut
CANNON_STEP = 10
LASER_SPEED = 1
ALIEN_SPEED = 0.3
ALIEN_SPAWN_INTERVAL = 1.2
DETECTION_RADIUS = 20
SCORE = 0
LIFE = 3
DIFFICULTY_LEVEL = 0  # Niveau de difficulté non sélectionné au début
paused = False  # Variable pour gérer la pause

# Listes pour les lasers et les extraterrestres
lasers = []
aliens = []
game_running = True
start_time = time.time()

# Configuration de la fenêtre
window = turtle.Screen()
window.setup(width=900, height=700)
window.bgcolor("black")
window.title("Space Invaders")
window.tracer(0)

def create_cannon():
    # Création du canon principal
    cannon = turtle.Turtle()
    cannon.penup()
    cannon.color("white")
    cannon.shape("square")
    cannon.setposition(0, -230)
    cannon.shapesize(stretch_wid=1, stretch_len=3)
    return cannon

def create_cannon_top():
    # Création de la partie supérieure du canon
    part2 = turtle.Turtle()
    part2.shape("square")
    part2.color("white")
    part2.penup()
    part2.speed(0)
    part2.setposition(0, -210)
    part2.shapesize(stretch_wid=1, stretch_len=1.5)
    return part2

def create_score_display():
    # Création de l'affichage du score
    score_display = turtle.Turtle()
    score_display.penup()
    score_display.hideturtle()
    score_display.setposition(350, 250)
    score_display.color("white")
    return score_display

# Utilisation des fonctions pour initialiser le canon et l'affichage du score
cannon = create_cannon()
part2 = create_cannon_top()
score_display = create_score_display()

def update_display():
    elapsed_time = time.time() - start_time
    score_display.clear()
    score_display.write(f"Temps : {elapsed_time:.1f} s\nScore : {SCORE}\nVies : {LIFE}", align="right", font=("Arial", 14, "normal"))

def create_alien():
    alien = turtle.Turtle()
    alien.penup()
    alien.shape("square")
    alien.color("green")
    alien.shapesize(stretch_wid=1.5, stretch_len=2)
    alien.setposition(0, 250)
    aliens.append(alien)
    return alien

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
            LIFE -= 1
            if LIFE <= 0:
                global game_running
                game_running = False

def create_laser():
    laser = turtle.Turtle()
    laser.penup()
    laser.color("red")
    laser.shape("square")
    laser.shapesize(stretch_wid=0.5, stretch_len=2)
    laser.setheading(90)
    laser.setposition(cannon.xcor(), cannon.ycor() + 20)
    lasers.append(laser)
    shoot_sound.play()
    return laser

def move_lasers():
    for laser in lasers[:]:
        laser.forward(LASER_SPEED)
        if laser.ycor() > window.window_height() / 2:
            laser.clear()
            laser.hideturtle()
            lasers.remove(laser)

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
                SCORE += 10
                collision_sound.play()
                explosion = turtle.Turtle()
                explosion.shape("circle")
                explosion.color("yellow")
                explosion.penup()
                explosion.setposition(alien.xcor(), alien.ycor())
                explosion.shapesize(stretch_wid=1, stretch_len=1)
                explosion.showturtle()
                window.update()
                time.sleep(0.2)
                explosion.hideturtle()
                break

def move_cannon(x):
    cannon.setx(x)
    part2.setx(x)

def move_left():
    x = cannon.xcor() - CANNON_STEP
    if x > -390:
        move_cannon(x)

def move_right():
    x = cannon.xcor() + CANNON_STEP
    if x < 390:
        move_cannon(x)

window.listen()
window.onkeypress(move_left, "Left")
window.onkeypress(move_right, "Right")
window.onkeypress(create_laser, "space")

def show_pause_menu():
    global paused
    paused = True
    
    # Affichage du menu de pause
    pause_text = turtle.Turtle()
    pause_text.hideturtle()
    pause_text.color("white")
    pause_text.penup()
    pause_text.setposition(0, 0)
    pause_text.write("Jeu en Pause\nAppuyez sur 'Échap' pour reprendre", align="center", font=("Arial", 24, "bold"))

    # Attendre que le jeu soit relancé
    while paused:
        window.update()
        time.sleep(0.01)
    
    # Effacer le menu de pause
    pause_text.clear()

def toggle_pause():
    global paused
    if not paused:
        show_pause_menu()
    else:
        paused = False

window.onkeypress(toggle_pause, "Escape")

def show_menu():
    global ALIEN_SPEED, ALIEN_SPAWN_INTERVAL, LASER_SPEED, DIFFICULTY_LEVEL
    
    # Affichage du logo "Space Invaders"
    logo = turtle.Turtle()
    logo.hideturtle()
    logo.color("yellow")
    logo.penup()
    logo.setposition(0, 200)
    logo.write("SPACE INVADERS", align="center", font=("Arial", 30, "bold"))

    # Boutons pour choisir le niveau de difficulté
    button1 = turtle.Turtle()
    button1.shape("square")
    button1.color("green")
    button1.shapesize(stretch_wid=1.5, stretch_len=5)
    button1.penup()
    button1.setposition(-150, 0)
    
    button2 = turtle.Turtle()
    button2.shape("square")
    button2.color("orange")
    button2.shapesize(stretch_wid=1.5, stretch_len=5)
    button2.penup()
    button2.setposition(0, 0)
    
    button3 = turtle.Turtle()
    button3.shape("square")
    button3.color("red")
    button3.shapesize(stretch_wid=1.5, stretch_len=5)
    button3.penup()
    button3.setposition(150, 0)

    text = turtle.Turtle()
    text.hideturtle()
    text.color("white")
    text.penup()
    text.setposition(0, -50)
    text.write("Choisissez le niveau de difficulté", align="center", font=("Arial", 18, "normal"))

    def set_difficulty(level):
        global ALIEN_SPEED, ALIEN_SPAWN_INTERVAL, LASER_SPEED, DIFFICULTY_LEVEL
        if level == 1:
            ALIEN_SPEED = 1
            ALIEN_SPAWN_INTERVAL = 3
            LASER_SPEED = 5
        elif level == 2:
            ALIEN_SPEED = 2
            ALIEN_SPAWN_INTERVAL = 1.0
            LASER_SPEED = 5
        elif level == 3:
            ALIEN_SPEED = 3
            ALIEN_SPAWN_INTERVAL = 0.7
            LASER_SPEED = 5
        DIFFICULTY_LEVEL = level
        logo.clear()
        text.clear()
        button1.hideturtle()
        button2.hideturtle()
        button3.hideturtle()

    button1.onclick(lambda x, y: set_difficulty(1))
    button2.onclick(lambda x, y: set_difficulty(2))
    button3.onclick(lambda x, y: set_difficulty(3))

    while DIFFICULTY_LEVEL == 0:
        window.update()
        time.sleep(0.01)

show_menu()

alien_timer = time.time()
while game_running:
    if time.time() - alien_timer > ALIEN_SPAWN_INTERVAL:
        create_alien()
        alien_timer = time.time()
    if not paused:
        move_aliens()
        move_lasers()
        check_collision()
        update_display()
        window.update()
    time.sleep(0.01)

game_over_sound.play()

game_over = turtle.Turtle()
game_over.hideturtle()
game_over.color("red")
game_over.penup()
game_over.setposition(0, 0)
game_over.write("GAME OVER", align="center", font=("Arial", 24, "bold"))

def save_score(username, score):
    score_data = {"username": username, "score": score}
    scores_collection.insert_one(score_data)

username = input("Entrez votre pseudo : ")
save_score(username, SCORE)

def display_leaderboard():
    scores = scores_collection.find().sort("score", -1).limit(10)  # Récupérer les 10 meilleurs scores
    print("Leaderboard:")
    for score in scores:
        print(f"{score['username']}: {score['score']}")

window.update()
window.mainloop()
