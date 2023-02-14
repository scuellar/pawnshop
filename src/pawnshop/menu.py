"""
Main menu for pawnshop
"""
import pygame
import pygame_menu
from pygame_menu.examples import create_example_window
from module.all_modules import available_modules
from typing import Tuple, Any
import main

surface = create_example_window('Pawnshop menu', (600, 400))
pygame_menu.themes.THEME_BLUE.widget_font_size =  12
#theme = widget_font_size
menu = pygame_menu.Menu(
    height=300,
    theme=pygame_menu.themes.THEME_BLUE,
    title='Welcome to Pawnshop',
    width=400
)


def choose_module(value, module):
    global THE_MODULE
    THE_MODULE = module
    print("Chose:", THE_MODULE)
    
def start_the_game() -> None:
    """
    Function that starts a game. This is raised by the menu button,
    here menu can be disabled, etc.
    """
    # Define globals
    global menu
    global THE_MODULE

    # Reset main menu and disable
    # You also can set another menu, like a 'pause menu', or just use the same
    # main_menu as the menu that will check all your input.
    menu.disable()
    menu.full_reset()

    print("starting")
    main.running_the_game(THE_MODULE, menu)
    
    # while True:

    #     # Application events
    #     events = pygame.event.get()
    #     for e in events:
    #         if e.type == pygame.QUIT:
    #             exit()
    #         elif e.type == pygame.KEYDOWN:
    #             if e.key == pygame.K_ESCAPE:
    #                 menu.enable()

    #                 # Quit this function, then skip to loop of main-menu on line 221
    #                 return

    #     # Pass evento main_menu
    #     if menu.is_enabled():
    #         menu.update(events)

menu.add.dropselect("Module: ",
                    available_modules,
                    #default = ,
                    onchange=choose_module)
menu.add.button('Next', start_the_game)
menu.add.button('Quit', pygame_menu.events.EXIT)

if __name__ == '__main__':
    menu.mainloop(surface)
