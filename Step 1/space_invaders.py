# -*- coding : utf-8 -*-
import turtle

# Création de la fen ê tre
window = turtle.Screen()
window.setup(width=800, height=600) # Taille de la fen ê tre
window.bgcolor("green") # Couleur de fond
window.title("Space Invaders")

# Création du canon
cannon = turtle.Turtle()
cannon.shape("square")
cannon.color("white")
cannon.penup() # Évite de dessiner des lignes pendant les déplacements
cannon.setposition(0 , -250) # Position en bas de l’écran

# Garder l ’écran ouvert
turtle.done()
