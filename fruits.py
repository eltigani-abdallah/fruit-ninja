import pygame 
import random
import os

# Définir le chemin du dossier du script
BASE_DIR = os.path.dirname(__file__)

# Vérification du répertoire de travail actuel
print("Répertoire de travail actuel :", os.getcwd())

# Initialisation de pygame
pygame.init()

# Dimensions de l'écran
LARGEUR_ECRAN = 1200
HAUTEUR_ECRAN = 600
screen = pygame.display.set_mode((LARGEUR_ECRAN, HAUTEUR_ECRAN))
pygame.display.set_caption('Fruit Ninja')

# Fond d'écran
try:
    image_fond = pygame.image.load(os.path.join(BASE_DIR, "background.jpg"))
    image_fond = pygame.transform.scale(image_fond, (LARGEUR_ECRAN, HAUTEUR_ECRAN))
except FileNotFoundError:
    print("background.jpg introuvable.")
    pygame.quit()
    exit()

# Chargement des images de fruits
noms_fruits = ["1.png", "2.png", "3.png", "4.png", "5.png", "6.png", "7.png", "8.png", "9.png", "10.png", "11.png", "111.png", "b1.png", 
               "b2.png", "gl2.png"]

images_fruits = []
for nom in noms_fruits:
    try:
        chemin_image = os.path.join(BASE_DIR, nom)
        images_fruits.append(pygame.image.load(chemin_image))
    except FileNotFoundError:
        print(f"Erreur de chargement : fichier {nom} introuvable !")
        pygame.quit()
        exit()

# Classe pour les fruits
class Fruit:
    def __init__(self, image, x, y, vitesse_x, vitesse_y, gravite):
        self.image = pygame.transform.scale(image, (120, 120))  # Taille du fruit
        self.x = x
        self.y = y
        self.vitesse_x = vitesse_x
        self.vitesse_y = vitesse_y
        self.gravite = gravite
        self.actif = True

    def deplacer(self):
        if self.actif:
            self.x += self.vitesse_x
            self.y -= self.vitesse_y  # Lancement vers le haut
            self.vitesse_y -= self.gravite  # La gravité ralentit la montée et accélère la chute

            # Si le fruit sort de l'écran par le bas, on le désactive
            if self.y > HAUTEUR_ECRAN:
                self.actif = False

    def dessiner(self, surface):
        if self.actif:
            surface.blit(self.image, (self.x, self.y))

# Fonction pour créer un lot de fruits
def creer_lot_fruits(taille_lot):
    fruits = []
    for _ in range(taille_lot):
        x = random.randint(100, LARGEUR_ECRAN - 100)  # Position X de départ
        y = HAUTEUR_ECRAN  # Les fruits commencent en bas
        vitesse_x = random.uniform(-5, 5)  
        vitesse_y = random.uniform(16, 20)  
        gravite = 0.35  # Force de gravité
        image_fruit = random.choice(images_fruits)
        fruits.append(Fruit(image_fruit, x, y, vitesse_x, vitesse_y, gravite))
    return fruits

# Variables du jeu
lots_fruits = [1, 1, 2, 2, 3, 2, 3, 3, 4, 2, 5, 3, 3, 4, 5, 3, 5, 2, 4, 2, 5, 3, 7, 4, 5, 3, 6, 1]  # Séquence des lots
lot_actuel = 0
fruits = []
timer_prochain_lot = 0
intervalle_lots = 2000  # Intervalle entre les lots (en millisecondes)

# Horloge pour gérer les FPS
horloge = pygame.time.Clock()
temps_depart = pygame.time.get_ticks()

# Boucle du jeu
jeu_en_cours = True
while jeu_en_cours:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            jeu_en_cours = False

    # Mise à jour de l'écran
    screen.blit(image_fond, (0, 0))

    # Vérifier s'il est temps d'ajouter un nouveau lot de fruits
    temps_actuel = pygame.time.get_ticks()
    if temps_actuel - timer_prochain_lot > intervalle_lots and lot_actuel < len(lots_fruits):
        timer_prochain_lot = temps_actuel
        taille_lot = lots_fruits[lot_actuel]
        fruits.extend(creer_lot_fruits(taille_lot))
        lot_actuel += 1

    # Déplacement et dessin des fruits
    for fruit in fruits:
        fruit.deplacer()
        fruit.dessiner(screen)

    # Suppression des fruits inactifs
    fruits = [fruit for fruit in fruits if fruit.actif]

    pygame.display.flip()
    horloge.tick(60)  

pygame.quit()

