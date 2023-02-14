import pygame
import virtual_board as VB

###########
# Game init
###########

def done(vb):
    pygame.display.quit()
    pygame.quit()
    vb.on_board_exit()


# Game loop
def running_the_game(module, menu):

    module_instance = module()    
    print ("Started module ", module_instance.get_name())

    vb = VB.VBoard(module_instance)
    running = True
    while running:
        for event in pygame.event.get():
            ###############
            # GUI EVENTS:
            ###############
    
            # Close the game 
            if event.type == pygame.QUIT:
                running = False
    
            # Press Q to quit
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                running = False
    
            # Press F to quit
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                vb.flip_board = not vb.flip_board
            
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                menu.enable()
                
            # Mouse click
            elif event.type == pygame.MOUSEBUTTONDOWN:
    
                # Left Click
                if event.button == 1: # Left mouse button
                    # Get the row and column of the square that was clicked
                    row, col = event.pos[1] // 64, event.pos[0] // 64
    
                    vb.left_click(row,col)
                    
        # If menu enabled, go back to main menue
        if menu.is_enabled():
            menu.update()
            
        vb.draw_board()
        vb.rest()
        
    # Quit game engine
    done(vb)

if __name__ == '__main__':
    print("DONE")
