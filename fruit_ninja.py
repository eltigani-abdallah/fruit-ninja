import pygame 
import random
import os
import string
from time import sleep
import pygame_menu
from pygame_menu import themes

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Fruit Ninja')

# Define the script directory path
BASE_DIR = ".\\"

#Function to return to the main menu
def return_to_main_menu():
    second_menu.close()
    menu()
    
def set_difficulty(value, difficulty):
    global difficulty_level
    difficulty_level = difficulty  # Store the selected difficulty level
    print(f"Selected Difficulty: {value}, Difficulty Level: {difficulty_level}")
    


#Starts the game and initializes the loading bar properly
def start_the_game():
    loading.get_widget("1").set_value(0) # Reset the loading bar to 0
    mainmenu._open(loading)
    pygame.time.set_timer(update_loading, 30) # Restart the loading timer

    try:
        game_loop(difficulty_level)  # Pass the difficulty level when starting the game
    except NameError:
        game_loop(1)
    
# Navigate to the level menu
def level_menu():
    mainmenu._open(level)

# Create a custom theme for the menu
mytheme = pygame_menu.themes.THEME_DARK.copy()
mytheme.background_color=(0, 0, 0, 0)
mytheme.title_background_color=(0, 0, 0)
font = pygame_menu.font.FONT_8BIT
mytheme.widget_font = font
font_title = pygame_menu.font.FONT_DIGITAL
mytheme.title_font = font_title
mainmenu = pygame_menu.Menu('Welcome', 1200, 600, theme=mytheme)

# Main menu
mainmenu.add.text_input('Name: ', default='username')
mainmenu.add.button('Play', start_the_game)
mainmenu.add.button('Levels', level_menu)
mainmenu.add.button('Quit', pygame_menu.events.EXIT)

# Secondary menu with Restart, Return, and Quit options
second_menu = pygame_menu.Menu('Game Options', 1200, 600, theme=mytheme)
second_menu.add.button('Restart Game', start_the_game)
second_menu.add.button('Return to Main Menu', return_to_main_menu)
second_menu.add.button('Quit', pygame_menu.events.EXIT) 

# Level selection menu
level = pygame_menu.Menu('Select a Difficulty', 1200, 600, theme=mytheme)
level.add.selector('Difficulty :', [('Easy', 1), ('Medium', 2), ('Hard', 3)], onchange=set_difficulty)

# Loading screen menu
loading = pygame_menu.Menu('Loading the Game...', 1200, 600, theme=mytheme)
loading.add.progress_bar("Progress", progressbar_id = "1", default=0, width = 200, )

# Arrow selection widget for the menu
arrow = pygame_menu.widgets.LeftArrowSelection(arrow_size = (10, 15))

# Event constant for updating the loading bar
update_loading = pygame.USEREVENT + 0

#Handles the main menu and transitions to game
def menu():
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == update_loading:
                progress = loading.get_widget("1")
                if progress.get_value() < 100:
                    progress.set_value(progress.get_value() + 1)
                else:    
                    pygame.time.set_timer(update_loading, 0)
                    game_loop()
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
                
        # Display the background image
        screen.blit(background_image, (0, 0))        
    
        if mainmenu.is_enabled():
            mainmenu.update(events)
            mainmenu.draw(screen)
            if (mainmenu.get_current().get_selected_widget()):
                arrow.draw(screen, mainmenu.get_current().get_selected_widget())
                
        pygame.display.update()         


def secondMenu():
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == update_loading:
                progress = loading.get_widget("1")
                if progress.get_value() < 100:
                    progress.set_value(progress.get_value() + 1)
                else:
                    pygame.time.set_timer(update_loading, 0)
                    game_loop()  # Correctly restart the game loop
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
                
        # Display the background image
        screen.blit(background_image, (0, 0))        
    
        if second_menu.is_enabled():
            second_menu.update(events)
            second_menu.draw(screen)
            if (second_menu.get_current().get_selected_widget()):
                arrow.draw(screen, second_menu.get_current().get_selected_widget())
        
        pygame.display.update()        



# Load sounds
pygame.mixer.init()
background_music = os.path.join(BASE_DIR, "assets\\sound\\chinatown-chinese-new-year-celebration-276682 (1).mp3")
sound_fruit = pygame.mixer.Sound(os.path.join(BASE_DIR, "assets\\sound\\S0000017.NSF_00016.wav"))
sound_bomb = pygame.mixer.Sound(os.path.join(BASE_DIR, "assets\\sound\\S0000003.NSF_00035.wav"))
sound_keypress = pygame.mixer.Sound(os.path.join(BASE_DIR, "assets\\sound\\S000000C.NSF_00038.wav"))
sound_explosion = pygame.mixer.Sound(os.path.join(BASE_DIR, "assets\\sound\\S0000038.NSF_00031.wav"))
sound_ice = pygame.mixer.Sound(os.path.join(BASE_DIR, "assets\\sound\\Crystal_Blocker_Vanish.wav"))
sound_pomegranate = pygame.mixer.Sound(os.path.join(BASE_DIR, "assets\\sound\\S0000004.NSF_00000.wav"))

# Play background music
pygame.mixer.music.load(background_music)
pygame.mixer.music.play(-1)  # Loop indefinitely
pygame.mixer.music.set_volume(0.3) 


#Color definitions
WHITE=(255,255,255)

#List of all uppercase letters A-Z
letter_list=list(string.ascii_uppercase)

#images to represent lives
lives3img=pygame.image.load(os.path.join(BASE_DIR, "assets\\lives\\strike0.png"))
lives3img=pygame.transform.scale(lives3img, (175,120))

lives2img=pygame.image.load(os.path.join(BASE_DIR, "assets\\lives\\strike1.png"))
lives2img=pygame.transform.scale(lives2img, (175,120))

lives1img=pygame.image.load(os.path.join(BASE_DIR, "assets\\lives\\strike2.png"))
lives1img=pygame.transform.scale(lives1img, (175,120))

lives0img=pygame.image.load(os.path.join(BASE_DIR, "assets\\lives\\strike3.png"))
lives0img=pygame.transform.scale(lives0img, (175,120))



# Background image
try:
    background_image = pygame.image.load(os.path.join(BASE_DIR, "assets\\background\\background1.jpg"))
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
except FileNotFoundError:
    print("background.jpg not found.")
    pygame.quit()
    exit()

# Load fruit images
fruit_names = ["kiwi.png", "pineapple.png", "grape.png", "lemon.png", "watermelon.png", "orange.png", "passionfruit.png", "mango.png", "strawberry.png", "dragonfruit.png", "banana.png", "pomegranate.png", 
"bomb.png", "ice.png"]

fruit_images = []


for name in fruit_names:


    try:
        image_path = os.path.join(BASE_DIR,"assets\\fruit", name)
        fruit_images.append(pygame.image.load(image_path))
    except FileNotFoundError:
        print(f"Loading error: file {name} not found!")
        pygame.quit()
        exit()


# Function to draw text with a white outline
def draw_text(surface, text,pos, size=60, color=(255,255,255), font=None):
    '''draw text on top of surface'''
    if font is None:
        font=pygame.font.Font(None, size)
        
    text_surface=font.render(text, True,color)
    text_outline = font.render(text, True, (0, 0, 0))
    surface.blit(text_outline, (pos[0] - 2, pos[1] - 2))
    surface.blit(text_outline, (pos[0] + 2, pos[1] - 2))
    surface.blit(text_outline, (pos[0] - 2, pos[1] + 2))
    surface.blit(text_outline, (pos[0] + 2, pos[1] + 2))
    surface.blit(text_surface, pos)


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
        
        # Play appropriate sound based on fruit type
        if self.type == "bomb":
            sound_bomb.play()
        if self.type == "ice":
            sound_ice.play()
        else:
            sound_fruit.play()
            
    # Move the fruit based on speed and gravity    
    def move(self):
        if self.active:
            self.x += self.speed_x
            self.y -= self.speed_y  # Launching upwards
            self.speed_y -= self.gravity  # Gravity slows down ascent and speeds up fall

    # Draw the fruit and the associated letter on the screen
    def draw(self, surface):
            
        if self.active:
            surface.blit(self.image, (self.x, self.y))
            draw_text(surface,self.letter,(self.x+40,self.y+40),50, (255,255,255))



# Function to create a batch of fruits
def create_fruit_batch(batch_size, difficulty_level):
    fruits = []
    letter_list=list(string.ascii_uppercase)
    if len(letter_list)==0:
        letter_list=list(string.ascii_uppercase)
    bomb_letter=random.choice(letter_list)
    letter_list.remove(bomb_letter)
    for _ in range(batch_size * difficulty_level):
        x = random.randint(400, SCREEN_WIDTH - 400)  # Starting X position
        y = SCREEN_HEIGHT  # Fruits start at the bottom
        speed_x = random.uniform(-3, 3) 
        speed_y = random.uniform(7, 10) 
        gravity = 0.10  # Gravity force
        fruit_image = random.choice(fruit_images)
        fruit_name=fruit_names[fruit_images.index(fruit_image)]

        if "ice" in fruit_name.lower():
            fruit_type="ice"

        elif "bomb" in fruit_name.lower():
            fruit_type="bomb"
        
        else:
            fruit_type="fruit"

        if fruit_type=="bomb":
            fruit_letter=bomb_letter
        else:
            fruit_letter=random.choice(letter_list)
            letter_list.remove(fruit_letter)
        fruits.append(Fruit(fruit_image, x, y, speed_x, speed_y, gravity, fruit_letter, fruit_type))
    return fruits


def game_loop(difficulty_level):
# Game variables
    fruit_batches = [1, 1, 1, 1, 2, 2, 1, 1, 2, 1, 2, 1, 1, 2, 2, 1, 2, 2, 1, 2, 1, 1, 1, 2, 2,\
                    2, 2, 1, 3, 2, 2, 4, 3, 4, 2, 1, 2, 1, 2, 3, 2, 2, 1, 2, 1, 2, 3, 3]  # Sequence of batches
    current_batch = 0
    fruits = []
    next_batch_timer = 0
    batch_interval = 2500  # Interval between batches (in milliseconds)

    clock = pygame.time.Clock()

    score=0

    game_running = True
    lives=3
    slow_mode=False
    slow_end=0

    combo_message=""
    combo_display_time=0
    
    while game_running:
        current_time = pygame.time.get_ticks()

        keys=pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
            mainmenu.reset(1)  # Reset to main menu properly**
            pygame.time.set_timer(update_loading, 0)
            return

        # Draw the background
        screen.blit(background_image, (0, 0))
        draw_text(screen,f"Score: {score}",(0,0), 50,WHITE)

        if lives==3:
            screen.blit(lives3img, (1025,0))
        if lives==2:
            screen.blit(lives2img, (1025,0))
        if lives==1:
            screen.blit(lives1img, (1025,0))
        if lives==0:
            screen.blit(lives0img, (1025,0))

        for fruit in fruits:
            if fruit.y>=SCREEN_HEIGHT:
                match fruit.type:
                    case "bomb":
                        fruit.active=False
                    case "ice":
                        fruit.active=False
                    case _:
                        lives-=1
                        fruit.active=False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
                pygame.quit()
                exit()
            if event.type==pygame.KEYDOWN:
                pinput=event.unicode.upper()
                fruit_hit=[fruit for fruit in fruits if fruit.active and pinput==fruit.letter]

                if len(fruit_hit)>=3:
                    combo_message=f"COMBO X{len(fruit_hit)}"
                    combo_display_time=pygame.time.get_ticks()+2000
                    bonus_score=2 if len(fruit_hit)==3 else 3
                    score+= bonus_score
                
                for fruit in fruit_hit:
                    #print(f"Detected fruit: {fruit.letter}, Type: {fruit.type}")
                    if fruit.type== "bomb":
                        lives=-1
                        fruit.active=False
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
            fruits.extend(create_fruit_batch(batch_size, difficulty_level))  # Pass the difficulty level
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
        
        if combo_message and current_time<combo_display_time:
            draw_text(screen, combo_message,(0, 50), 25, (255,255,0))
        elif current_time>=combo_display_time:
            combo_message=""
            combo_display_time=0

        # Move and draw the fruits
        for fruit in fruits:
            fruit.move()
            fruit.draw(screen)

        # Remove inactive fruits
        fruits = [fruit for fruit in fruits if fruit.active]

        if lives<0:
            #placeholder loss screen
            draw_text(screen,"GAME OVER",(400, SCREEN_HEIGHT/2), 100, WHITE)
            mainmenu.reset(1)  # Reset to main menu properly**
            pygame.time.set_timer(update_loading, 0)
            secondMenu()
            return

        pygame.display.flip()
        clock.tick(60)

menu()

pygame.quit()