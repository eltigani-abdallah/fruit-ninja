import pygame
import random


pygame.init()


SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Fruit Ninja ')


BLANC = (255, 255, 255)
NOIR = (0, 0, 0)


background_image = pygame.image.load("background.jpg")
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))  


fruits = ['banan', 'citron', 'onion', 'mango']
special_items = ['Glaçon', 'Bombe']
combo_points = [1, 2, 3, 4, 5] 


clock = pygame.time.Clock()

jeu_marche = True


while jeu_marche:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            jeu_marche = False
        if event.type == pygame.KEYDOWN:
            print("Touche tapée :", event.unicode)

   
    screen.blit(background_image, (0, 0))  
    
   
    pygame.display.flip()

    
    clock.tick(10000)

pygame.quit()
