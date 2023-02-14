"""Virtual Board implements all the visual and interactive methods for
the GUI.

On on side, `pygame` calls `VBoard` to resolve any event that has to
do with the chess board.  On the other side, `VBoard` calls on a
`ChessModule` to resolve any game mechanincs.

This file also implements Board skins, which allow to change how the
boar looks. It's a good idea to move those into their own module if we
are going to expand on them

"""
import pygame
import chess
import module.module as M
import module.everyman_module as EM
import module.opening_practice as OP
import module.stockfish as SF

##############
# Board Skins
##############

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

mod1 = OP.OpeningPracticeModule
mod2 = EM.EverymanModule
mod3 = SF.StockfishModule
default_module = M.ModuleProduct3(mod1, mod2, mod3) #SF.StockfishModule # OP.OpeningPracticeModule # EM.EverymanModule # M.PvP

################
# Virtual Boarddo
################


class VBoard:
    def __init__(self):
        self.selected_square = -1  #-1 is None
        self.selected_piece  = None
        # If you want to play form the black side
        self.flip_board = False

        # How the board looks like 
        self.board_skin = default_skin
        self.square_size = 64 #pixels
        
        # Initialize game engine
        pygame.init()

        # Set screen size
        self.screen = pygame.display.set_mode((8 * self.square_size, 8 * self.square_size))

        # Define the module to play with
        self.module = default_module # Creates an instance of the module

    def try_move(self, target_square):
        return self.module.try_move(self.selected_square, target_square)
    
        # If there is a piece in the selected square
    def try_select(self, square):
        can_select = self.module.try_select(square)
        if can_select:
            self.selected_piece = self.module.piece_at(square)
            self.selected_square = chess.SQUARES[square]
            print("SELECTED:", self.selected_piece, "/n at: ", square)
        return can_select
    
    def deselect(self):
        self.selected_piece = None
        self.selected_square = -1
        print("DESELECTED")

    def sq2coor(self, square:int) -> (int, int):
        """Get the row and column from a square"""
        col = 7 - square % 8
        row = (square // 8)
        if not self.flip_board:
            col = 7-col
            row = 7-row
        return (row,col)
            
    def coor2sq(self, row:int, col:int) -> int:
        """Get the square from row and column"""
        if not self.flip_board:
            row = 7-row
        else:
            col = 7-col
        square = row * 8 + col
        return (square)
    
    def left_click(self, row, col):
        """ Update the board when a click happens."""
        
        # Figure out the square
        square = self.coor2sq(row,col)

        # Try to move
        moved = self.try_move(square)

        #Try to select a valid piece (i.e of the right color)
        selected = self.try_select(square)

        # If you didn't select, you deselect.
        if moved or not selected:
            self.deselect()

    def on_board_exit(self):
        self.module.on_exit()
        print("Goodbye!")
        
    def rest(self):
        self.module.wait_action()
        
    def draw_board(self):
        # Clear screen
        self.screen.fill(self.board_skin.white)
    
        # Draw chess board
        for square in chess.SQUARES:
            # Thses colomns display the board from blacks prespective
            (row, col) = self.sq2coor(square)
    
            # If this square is a light one
            is_light = (col + row) % 2 == 1
    
            # Find the color of the square
            if is_light:
                square_color = self.board_skin.white
            else:
                square_color = self.board_skin.black
            
            if self.selected_square == square:
                if is_light:
                    square_color = self.board_skin.white_selected
                else:
                    square_color = self.board_skin.black_selected
            elif self.module.last_move():
                last_move = self.module.last_move() 
                if square in [last_move.from_square, last_move.to_square]:
                    if is_light:
                        square_color = self.board_skin.white_highlight
                    else:
                        square_color = self.board_skin.black_highlight
    
    
            #Draw one square
            # This could be optimized with a fixed background :P
            pygame.draw.rect(self.screen, square_color, (col * 64, row * 64, 64, 64))

            piece = self.module.piece_at(square)
            if piece:
                self.screen.blit(self.board_skin.images[piece.symbol()], (col * 64, row * 64))
    
        # Update screen
        pygame.display.flip()
