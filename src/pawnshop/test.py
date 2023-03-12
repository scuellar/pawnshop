import pygame
import pygame_gui
import menu
import module.all_modules as modules
import virtual_board as VB
import sys

pygame.init()
pygame.display.set_caption('PawnShop')

menu_active = True
THE_MODULE = modules.default_module

# Global instances
chess_board = VB.VBoard()
dimensions = chess_board.dimensions
window_surface = pygame.display.set_mode(dimensions)

main_menu_handler = menu.MenuHandler(dimensions, window_surface)
config_menu_handler = menu.MenuHandler(dimensions, window_surface)



background = pygame.Surface(dimensions)
background.fill(pygame.Color('#000000'))

clock = pygame.time.Clock()
is_running = True
def done ():
    chess_board.on_board_exit()
    pygame.display.quit()
    pygame.quit()
    exit()

i = 0
try:
    while is_running:
        time_delta = clock.tick(60)/1000.0
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                is_running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                is_running = False
                done()
                break
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                main_menu_handler.enable()

        pygame.display.update()
except Exception as e:
    print("Exception:", e)
    
        
done()
