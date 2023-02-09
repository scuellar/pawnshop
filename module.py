""" Modules are pluggins for PawnShop, they can implement different ways to play the game:

Examples:
- Local PvP
- Against an engine
- Practice openings
- Play online (through lichess)

"""
import chess

################
# Game Modules
################

class GameModule:
    def try_move(self, board, source_sq, target_sq) -> bool:
        raise Exception("Function not defined in Game Module: `try_move`.")
    
    def try_select(self, board, square):
        raise Exception("Function not defined in Game Module: `try_select`.")

####################
# Some basic modules
####################

# + Local Player vs. Player
class PvP(GameModule):
    """ Player vs. Player

    The basic module to play locally on the same screen
    """
    def __init__(self):
        pass

    def try_move(self, board, source_sq, target_sq) -> bool:
        if source_sq >= 0:
            move = chess.Move(source_sq, target_sq)
            # For now we only support promoting to queen (automatically)
            move_promo = chess.Move(source_sq, target_sq, chess.QUEEN)
            if board.is_legal(move):
                board.push(move)
                return True
            elif board.is_legal(move_promo):
                board.push(move_promo)
                return True
            else:
                print ("Not a legal move", move)
        return False

    def try_select(self, board, square):
        if board.piece_at(square):
            if board.piece_at(square).color == board.turn:
                # Set selected piece
                return True
        return False
    

# + Engine module
class PvE(PvP):
    """Player vs. Environment

    This module is a combinator to build modules where the player
    plays agains something else, such as:
    - Engine
    - Online opponenet
    - Oppening tree
    - Database
    """
    can_change_sides = True
    
    def __init__(self):
        self.player_color = chess.WHITE
        
    def change_side(self):
        if self.can_change_sides:
            if self.player_color == chess.WHITE:
                self.player_color = chess.BLACK
            else:
                self.player_color = chess.WHITE
        
    def try_move(self, board, source_sq, target_sq) -> bool:
        # If it's not your turn you cna't move
        if board.turn != self.player_color:
            return False

        # If it is your turn, try to move in the normal way
        result = PvP.try_move(self, board, source_sq, target_sq)

        if result:
            self.opponent_move(board)
        return result 

    def opponent_move(self, board):
        raise Exception("Function not defined in PvE module: `opponent_move`.")
    
    def try_select(self, board, square):
        # If it's not your turn you can't select
        if board.turn != self.player_color:
            return False
        # If it is your turn, try to select in the normal way
        return PvP.try_select(self,board,square)
    
