import pygame 
import random
import os
import string

# Define the script directory path
BASE_DIR = os.path.dirname(__file__)

# Check the current working directory
print("Current working directory:", os.getcwd())

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Fruit Ninja')

WHITE=(255,255,255)
BLACK=(0,0,0)
LIGHTBLUE=(173,216,230)

#list of all uppercase letters A-Z
letter_list=list(string.ascii_uppercase)

#score and lives for gameplay loop
score=0


# Background image
try:
    background_image = pygame.image.load(os.path.join(BASE_DIR, "background.jpg"))
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
except FileNotFoundError:
    print("background.jpg not found.")
    pygame.quit()
    exit()

# Load fruit images
fruit_names = ["kiwi.png", "pineapple.png", "grape.png", "lemon.png", "watermelon.png", "orange.png", "passionfruit.png", "mango.png", "strawberry.png", "dragonfruit.png", "banana.png", "pomegranate.png", 
"bomb2.png", "ice.png"]

fruit_images = []
for name in fruit_names:
    try:
        image_path = os.path.join(BASE_DIR, name)
        fruit_images.append(pygame.image.load(image_path))
    except FileNotFoundError:
        print(f"Loading error: file {name} not found!")
        pygame.quit()
        exit()

def print_text(surface,x,y, text, size, color, font=None):
    '''draw text on top of surface'''
    if font is None:
        font=pygame.font.Font(None, size)
        
    text_surface=font.render(text, True,color)
    surface.blit(text_surface, (x, y))


# Class for the fruits
class Fruit:
    def __init__(self, image, x, y, speed_x, speed_y, gravity, letter, type):
        self.image = pygame.transform.scale(image, (120, 120))  # Size of the fruit
        self.x = x
        self.y = y
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.original_speed_x= speed_x
        self.original_speed_y= speed_y
        self.gravity = gravity
        self.active = True
        self.letter= letter
        self.type= type
        
    def move(self):
        if self.active:
            self.x += self.speed_x
            self.y -= self.speed_y  # Launching upwards
            self.speed_y -= self.gravity  # Gravity slows down ascent and speeds up fall


    def draw(self, surface):
            
        if self.active:
            surface.blit(self.image, (self.x, self.y))
            print_text(surface, self.x,self.y,self.letter,50, (255,255,255))



# Function to create a batch of fruits
def create_fruit_batch(batch_size):
    fruits = []
    for _ in range(batch_size):
        x = random.randint(400, SCREEN_WIDTH - 400)  # Starting X position
        y = SCREEN_HEIGHT  # Fruits start at the bottom
        speed_x = random.uniform(-5, 5) 
        speed_y = random.uniform(16, 20) 
        gravity = 0.35  # Gravity force
        fruit_image = random.choice(fruit_images)
        fruit_name=fruit_names[fruit_images.index(fruit_image)]
        if "bomb" in fruit_name.lower():
            fruit_type="bomb"
        elif "ice" in fruit_name.lower():
            fruit_type="ice"
        else:
            fruit_type="fruit"
        fruit_letter=random.choice(letter_list)
        fruits.append(Fruit(fruit_image, x, y, speed_x, speed_y, gravity, fruit_letter, fruit_type))
    return fruits

# Game variables
fruit_batches = [1, 1, 2, 2, 3, 2, 3, 3, 4, 2, 5, 3, 3, 4, 5, 3, 5, 2, 4, 2, 5, 3, 7, 4, 5, 3, 6, 1]  # Sequence of batches
current_batch = 0
fruits = []
next_batch_timer = 0
batch_interval = 2000  # Interval between batches (in milliseconds)

# Clock to manage FPS
clock = pygame.time.Clock()
start_time = pygame.time.get_ticks()

# Game loop
# TODO add strike system using images

game_running = True
lives=3
slow_mode=False
slow_end=0
while game_running:
    current_time = pygame.time.get_ticks()

    # Draw the background
    screen.blit(background_image, (0, 0))
    print_text(screen, 0,0,f"Score: {score}", 50,WHITE)
    print_text(screen, 500, 0, f"lives: {lives}",50, WHITE)

    for fruit in fruits:
        if fruit.y>=SCREEN_HEIGHT and fruit.type!="bomb" and fruit.type!="ice":
            if not slow_mode:
                fruit.active=False
                lives-=1
                

                
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False
        if event.type==pygame.KEYDOWN:
            pinput=event.unicode.upper()
            if pinput=="Å":
                lives=3
            for fruit in fruits:
                if fruit.active and pinput==fruit.letter:
                    if fruit.type== "bomb":
                        fruit.active=False
                        lives=-1
                    elif fruit.type== "ice":
                        slow_mode=True
                        slow_end=pygame.time.get_ticks()+2000
                        fruit.active=False
                    else:
                        score+=1
                        fruit.active=False
            


    # Check if it's time to add a new batch of fruits
    
    if current_time - next_batch_timer > batch_interval and current_batch < len(fruit_batches):
        next_batch_timer = current_time
        batch_size = fruit_batches[current_batch]
        fruits.extend(create_fruit_batch(batch_size))
        current_batch += 1
    if slow_mode:
        for fruit in fruits:
            fruit.speed_y *= 0.5
            fruit.speed_x *= 0.5
    
    if slow_mode and current_time>slow_end:
        slow_mode=False
        for fruit in fruits:
            fruit.speed_x= fruit.original_speed_x
            fruit.speed_y= fruit.original_speed_y

    # Move and draw the fruits
    for fruit in fruits:
        fruit.move()
        fruit.draw(screen)

    # Remove inactive fruits
    fruits = [fruit for fruit in fruits if fruit.active]

    if lives<0:
        #placeholder loss screen
        print_text(screen, 400, SCREEN_HEIGHT/2, "GAME OVER", 100, WHITE)

    pygame.display.flip()
    clock.tick(60)
    #print(f"active fruits: {len(fruits)}")

pygame.quit()
