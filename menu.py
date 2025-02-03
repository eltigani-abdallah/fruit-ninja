from time import sleep
import pygame
import pygame_menu
from pygame_menu import themes
 
pygame.init()
surface = pygame.display.set_mode((800, 600))
 
try:
    background_image = pygame.image.load('background-menu.jpg')
    background_image = pygame.transform.scale(background_image, (800, 600))
except pygame.error as e:
    print(f"Erreur de chargement de l'image : {e}")
    exit()
 
def set_difficulty(value, difficulty):
    print(value)
    print(difficulty)
 
def start_the_game():
    mainmenu._open(loading)
    pygame.time.set_timer(update_loading, 30)
 
def level_menu():
    mainmenu._open(level)
 

mytheme = pygame_menu.themes.THEME_DARK.copy()
mytheme.background_color=(0, 0, 0, 0)
mytheme.title_background_color=(0, 0, 0)
font = pygame_menu.font.FONT_8BIT
mytheme.widget_font = font
font_title = pygame_menu.font.FONT_DIGITAL
mytheme.title_font = font_title

mainmenu = pygame_menu.Menu('Welcome', 800, 600, theme=mytheme)
mainmenu.add.text_input('Name: ', default='username')
mainmenu.add.button('Play', start_the_game)
mainmenu.add.button('Levels', level_menu)
mainmenu.add.button('Quit', pygame_menu.events.EXIT)
 
level = pygame_menu.Menu('Select a Difficulty', 800, 600, theme=mytheme)
level.add.selector('Difficulty :', [('Hard', 1), ('Medium' , 2), ('Easy', 3)], onchange=set_difficulty)
 
loading = pygame_menu.Menu('Loading the Game...', 800, 600, theme=mytheme)
loading.add.progress_bar("Progress", progressbar_id = "1", default=0, width = 200, )
 
arrow = pygame_menu.widgets.LeftArrowSelection(arrow_size = (10, 15))
 
update_loading = pygame.USEREVENT + 0

 
while True:
    events = pygame.event.get()
    for event in events:
        if event.type == update_loading:
            progress = loading.get_widget("1")
            progress.set_value(progress.get_value() + 1)
            if progress.get_value() == 100:
                pygame.time.set_timer(update_loading, 0)
        if event.type == pygame.QUIT:
            exit()
            
    # Afficher l'image de fond
    surface.blit(background_image, (0, 0))        
 
    if mainmenu.is_enabled():
        mainmenu.update(events)
        mainmenu.draw(surface)
        if (mainmenu.get_current().get_selected_widget()):
            arrow.draw(surface, mainmenu.get_current().get_selected_widget())
    
    pygame.display.update()        