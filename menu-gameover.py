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

# Secondary menu with Restart, Return, and Quit options
second_menu = pygame_menu.Menu('Game Options', 1200, 600, theme=mytheme)
second_menu.add.button('Restart Game', start_the_game)
second_menu.add.button('Return to Main Menu', return_to_main_menu)
second_menu.add.button('Quit', pygame_menu.events.EXIT) 
    
# Loading screen menu
loading = pygame_menu.Menu('Loading the Game...', 1200, 600, theme=mytheme)
loading.add.progress_bar("Progress", progressbar_id = "1", default=0, width = 200, )

# Arrow selection widget for the menu
arrow = pygame_menu.widgets.LeftArrowSelection(arrow_size = (10, 15))

# Event constant for updating the loading bar
update_loading = pygame.USEREVENT + 0
# Secondary menu with Restart, Return, and Quit options
second_menu = pygame_menu.Menu('Game Options', 1200, 600, theme=mytheme)
second_menu.add.button('Restart Game', start_the_game)
second_menu.add.button('Return to Main Menu', return_to_main_menu)
second_menu.add.button('Quit', pygame_menu.events.EXIT) 
    

secondMenu():
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
        
'''if lives<0:
            #placeholder loss screen
            draw_text(screen,"GAME OVER",(400, SCREEN_HEIGHT/2), 100, WHITE)
            mainmenu.reset(1)  # Reset to main menu properly**
            pygame.time.set_timer(update_loading, 0)
            secondMenu()
            return

        pygame.display.flip()
        clock.tick(60)        '''
        
        pygame.quit()