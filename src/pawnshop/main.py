import pygame
import virtual_board as VB
import pygame_menu
import sys

###########
# Game init
###########

def done(vb):
    vb.on_board_exit()
    print("HERE")
    pygame.display.quit()
    print("HERE2")
    pygame.quit()
    print("HERE3")
    sys.exit()
    print("HERE4")


# Game loop
def running_the_game(module, menu):

    module_instance = module()    
    print ("Started module ", module_instance.get_name())

    vb = VB.VBoard(module_instance)
    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            ###############
            # GUI EVENTS:
            ###############
    
            # Close the game 
            if event.type == pygame.QUIT:
                running = False
                done(vb)
    
            # Press Q to quit
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                running = False
    
            # Press F to quit
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                vb.flip_board = not vb.flip_board
            
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                menu.enable()
                print("ENABLED")
                
            # Mouse click
            elif event.type == pygame.MOUSEBUTTONDOWN:
    
                # Left Click
                if event.button == 1: # Left mouse button
                    # Get the row and column of the square that was clicked
                    row, col = event.pos[1] // 64, event.pos[0] // 64
    
                    vb.left_click(row,col)
                    
        # If menu enabled, go back to main menue
        if menu.is_enabled():
            menu.update(events)
            
        vb.draw_board()
        vb.rest()
        
    # Quit game engine
    done(vb)

if __name__ == '__main__':
    print("DONE")
