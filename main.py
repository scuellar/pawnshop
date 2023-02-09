import pygame
import chess
import virtual_board as VB


def done():
    pygame.display.quit()
    pygame.quit()

###########
# Game init
###########
vb = VB.VBoard()

# Game loop
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
            
        # Mouse click
        elif event.type == pygame.MOUSEBUTTONDOWN:

            # Left Click
            if event.button == 1: # Left mouse button
                # Get the row and column of the square that was clicked
                row, col = event.pos[1] // 64, event.pos[0] // 64

                vb.left_click(row,col)
                
            
    vb.draw_board()

# Quit game engine
done()
