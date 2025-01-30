
import pygame  
import random
import os
import string

# Define the script directory path
BASE_DIR = os.path.dirname(__file__)

# Initialize pygame
pygame.init()

# Load sounds
pygame.mixer.init()
background_music = os.path.join(BASE_DIR, "chinatown-chinese-new-year-celebration-276682 (1).mp3")
sound_fruit = pygame.mixer.Sound(os.path.join(BASE_DIR, "S0000017.NSF_00016.wav"))
sound_bomb = pygame.mixer.Sound(os.path.join(BASE_DIR, "S0000003.NSF_00035.wav"))
sound_keypress = pygame.mixer.Sound(os.path.join(BASE_DIR, "S000000C.NSF_00038.wav"))
sound_explosion = pygame.mixer.Sound(os.path.join(BASE_DIR, "S0000038.NSF_00031.wav"))
sound_ice = pygame.mixer.Sound(os.path.join(BASE_DIR, "Crystal_Blocker_Vanish.wav"))
sound_pomegranate = pygame.mixer.Sound(os.path.join(BASE_DIR, "S0000004.NSF_00000.wav"))

# Play background music
pygame.mixer.music.load(background_music)
pygame.mixer.music.play(-1)  # Loop indefinitely

# Screen dimensions
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Fruit Ninja')

letter_list = list(string.ascii_uppercase)

# Load background image
try:
    background_image = pygame.image.load(os.path.join(BASE_DIR, "background3.jpg"))
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
except FileNotFoundError:
    print("background3.jpg not found.")
    pygame.quit()
    exit()

# Load fruit images
fruit_names = ["kiwi.png", "pineapple.png", "grape.png", "lemon.png", "watermelon.png", "orange.png", "passionfruit.png", "mango.png", "strawberry.png", "dragonfruit.png", "banana.png", "pomegranate.png", "bomb1.png", "bomb2.png", "bomb3.png", "ice.png"]

fruit_images = []
for name in fruit_names:
    try:
        image_path = os.path.join(BASE_DIR, name)
        fruit_images.append(pygame.image.load(image_path))
    except FileNotFoundError:
        print(f"Loading error: file {name} not found!")
        pygame.quit()
        exit()

font = pygame.font.Font(None, 48)

def draw_text(surface, text, pos):
    text_surface = font.render(text, True, (255, 255, 255))
    text_outline = font.render(text, True, (0, 0, 0))
    surface.blit(text_outline, (pos[0] - 2, pos[1] - 2))
    surface.blit(text_outline, (pos[0] + 2, pos[1] - 2))
    surface.blit(text_outline, (pos[0] - 2, pos[1] + 2))
    surface.blit(text_outline, (pos[0] + 2, pos[1] + 2))
    surface.blit(text_surface, pos)

class Fruit:
    def __init__(self, image, x, y, speed_x, speed_y, gravity, letter, type):
        self.image = pygame.transform.scale(image, (120, 120))
        self.x = x
        self.y = y
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.gravity = gravity
        self.active = True
        self.letter = letter
        self.type = type
        
        if self.type == "bomb":
            sound_bomb.play()
        else:
            sound_fruit.play()

    def move(self):
        if self.active:
            self.x += self.speed_x
            self.y -= self.speed_y  
            self.speed_y -= self.gravity  
            if self.y > SCREEN_HEIGHT:
                self.active = False

    def draw(self, surface):
        if self.active:
            surface.blit(self.image, (self.x, self.y))
            draw_text(surface, self.letter, (self.x + 45, self.y + 45))

def create_fruit_batch(batch_size):
    fruits = []
    for _ in range(batch_size):
        x = random.randint(400, SCREEN_WIDTH - 400)
        y = SCREEN_HEIGHT
        speed_x = random.uniform(-5, 5)
        speed_y = random.uniform(16, 20)
        gravity = 0.35
        fruit_image = random.choice(fruit_images)
        fruit_name = fruit_names[fruit_images.index(fruit_image)]
        
        if "bomb" in fruit_name.lower():
            fruit_type = "bomb"
            fruit_letter = "B"
        elif "ice" in fruit_name.lower():
            fruit_type = "ice"
            fruit_letter = random.choice(letter_list)
        else:
            fruit_type = "fruit"
            fruit_letter = random.choice(letter_list)
        
        fruits.append(Fruit(fruit_image, x, y, speed_x, speed_y, gravity, fruit_letter, fruit_type))
    return fruits

fruit_batches = [1, 1, 2, 2, 3, 2, 3, 3, 4, 2, 5, 3, 3, 4, 5, 3, 5, 2, 4, 2, 5, 3, 7, 4, 5, 3, 6, 1]
current_batch = 0
fruits = []
next_batch_timer = 0
batch_interval = 2000
clock = pygame.time.Clock()
start_time = pygame.time.get_ticks()

game_running = True

while game_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False
        if event.type == pygame.KEYDOWN:
            sound_keypress.play()
            pinput = event.unicode.upper()
            for fruit in fruits:
                if fruit.active and pinput == fruit.letter:
                    if fruit.type == "bomb":
                        sound_explosion.play()
                        print("BOOM")
                        fruit.active = False
                    elif fruit.type == "ice":
                        sound_ice.play()
                        print("TOKI YO, TOMARE!!")
                    else:
                        fruit.active = False

    screen.blit(background_image, (0, 0))
    
    current_time = pygame.time.get_ticks()
    if current_time - next_batch_timer > batch_interval and current_batch < len(fruit_batches):
        next_batch_timer = current_time
        batch_size = fruit_batches[current_batch]
        fruits.extend(create_fruit_batch(batch_size))
        current_batch += 1

    for fruit in fruits:
        fruit.move()
        fruit.draw(screen)

    fruits = [fruit for fruit in fruits if fruit.active]
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
