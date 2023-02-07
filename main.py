import pygame
import chess
from sys import exit


BLACK_ROOK   = 'r'
BLACK_KNIGHT = 'n'
BLACK_BISHOP = 'b'
BLACK_QUEEN  = 'q'
BLACK_KING   = 'k'
BLACK_PAWN   = 'p'
WHITE_ROOK   = 'R'
WHITE_KNIGHT = 'N'
WHITE_BISHOP = 'B'
WHITE_QUEEN  = 'Q'
WHITE_KING   = 'K'
WHITE_PAWN   = 'P'


##############
# Board Skins
##############

# Load chess pieces
wiki_images = {}
wiki_images[BLACK_ROOK  ] = pygame.image.load("img/pieces/black_rook.png")
wiki_images[BLACK_KNIGHT] = pygame.image.load("img/pieces/black_knight.png")
wiki_images[BLACK_BISHOP] = pygame.image.load("img/pieces/black_bishop.png")
wiki_images[BLACK_QUEEN ] = pygame.image.load("img/pieces/black_queen.png")
wiki_images[BLACK_KING  ] = pygame.image.load("img/pieces/black_king.png")
wiki_images[BLACK_PAWN  ] = pygame.image.load("img/pieces/black_pawn.png")
wiki_images[WHITE_ROOK  ] = pygame.image.load("img/pieces/white_rook.png")
wiki_images[WHITE_KNIGHT] = pygame.image.load("img/pieces/white_knight.png")
wiki_images[WHITE_BISHOP] = pygame.image.load("img/pieces/white_bishop.png")
wiki_images[WHITE_QUEEN ] = pygame.image.load("img/pieces/white_queen.png")
wiki_images[WHITE_KING  ] = pygame.image.load("img/pieces/white_king.png")
wiki_images[WHITE_PAWN  ] = pygame.image.load("img/pieces/white_pawn.png")

default_color = (0,0,0)
class BoardSkin:
    def __init__(self,
                 black = default_color,
                 black_highlighted = default_color,
                 black_selected = default_color,
                 white = default_color,
                 white_highlight = default_color,
                 white_selected = default_color,
                 images = wiki_images
                ):
        self.black             = black              
        self.black_highlighted = black_highlighted  
        self.black_selected    = black_selected     
        self.white             = white              
        self.white_highlight   = white_highlight    
        self.white_selected    = white_selected     
        self.images            = images             

        
# Build our default skin
lichess_skin = BoardSkin()
lichess_skin.black = (239,217,181)
lichess_skin.black_highlight  = (172,162,73)
lichess_skin.black_selected  = (106,111,66)
lichess_skin.white = (180,136,99)
lichess_skin.white_highlight = (206,209,123)
lichess_skin.white_selected = (135,151,106)
lichess_skin.images = wiki_images

default_skin = lichess_skin

board_skin = default_skin




# Initialize game board
board = chess.Board()
selected_square = -1 # Starts with none
selected_piece  = None
# If you want to play form the black side
flip_board = False 

def try_move(board, selected_square, target_square):
    if selected_square >= 0:
        move = chess.Move(selected_square, square)
        # For now we only support promoting to queen (automatically)
        move_promo = chess.Move(selected_square, square, chess.QUEEN)
        if board.is_legal(move):
            board.push(move)
            return True
        elif board.is_legal(move_promo):
            board.push(move_promo)
            return True
        else:
            print ("Not a legal move", move)
    return False

# If there is a piece in the selected square
def try_select(board, square):
    global selected_square, selected_piece
    
    if board.piece_at(square):
        if board.piece_at(square).color == board.turn:
            # Set selected piece
            selected_piece = board.piece_at(square)
            selected_square = chess.SQUARES[square]
            print("SELECTED:", selected_piece, "/n at: ", row, col)
            return True
    return False


def deselect():
    global selected_piece, selected_square
    
    selected_piece = None
    selected_square = -1
    print("DESELECTED")


def draw_board(board):
    # Clear screen
    screen.fill(WHITE)

    # Draw chess board
    for square in chess.SQUARES:
        # Thses colomns display the board from blacks prespective
        col = chess.square_file(square)  
        row = chess.square_rank(square)

        if not flip_board:
            #If not flip, flip them to white's perspective
            col = 7-col
            row = 7-row

        # If this square is a light one
        is_light = (col + row) % 2 == 0

        # Find the color of the square
        if is_light:
            square_color = board_skin.white
        else:
            square_color = board_skin.black
        
        if selected_square == square:
            if is_light:
                square_color = board_skin.white_selected
            else:
                square_color = board_skin.black_selected
        elif board.move_stack:
            last_move = board.peek() 
            if square in [last_move.from_square, last_move.to_square]:
                if is_light:
                    square_color = board_skin.white_highlight
                else:
                    square_color = board_skin.black_highlight


                    
        pygame.draw.rect(screen, square_color, (col * 64, row * 64, 64, 64))

        piece = board.piece_at(square)
        if piece:
            screen.blit(images[piece.symbol()], (col * 64, row * 64))

    # Update screen
    pygame.display.flip()

###########
# Game init
###########

# Initialize game engine
pygame.init()

# Set screen size
screen = pygame.display.set_mode((512, 512))
    
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
            flip_board = not flip_board
            
        # Mouse click
        elif event.type == pygame.MOUSEBUTTONDOWN:

            # Left Click
            if event.button == 1: # Left mouse button
                # Get the row and column of the square that was clicked
                row, col = event.pos[1] // 64, event.pos[0] // 64
                if not flip_board:
                    col = 7-col
                    row = 7-row
                    
                square = row * 8 + col

                # Try to move
                moved = try_move(board, selected_square, square)

                #Try to select a valid piece (i.e of the right color)
                selected = try_select(board, square)

                # If nothing happened then deselect
                
                if not (moved or selected):
                    deselect()
            
    draw_board(board)

# Quit game engine
pygame.display.quit()
pygame.quit()
