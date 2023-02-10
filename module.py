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

    def wait_action(self, board):
        """ What to do when no action has been triggered.
        """
        pass

    def on_exit(self):
        pass

##################
# Modules that end
##################
class ModuleEnds:
    """
    For modules that end.

    These modules can be combined with other modules.
    """
    def __init__(self):
        self.ended = False

####################
# Combinators
####################
class ModuleProduct(GameModule):
    """
    Join two modules, the first one has to end
    """
    def __init__(self, mod1, mod2):
        self.mod1 = mod1()
        self.mod2 = mod2()

    def try_move(self, board, source_sq, target_sq) -> bool:
        if not self.mod1.ended:
            return self.mod1.try_move(board, source_sq, target_sq)
        else:
            return self.mod2.try_move(board, source_sq, target_sq)
        
    def try_select(self, board, square):
        if not self.mod1.ended:
            return self.mod1.try_select(board, square)
        else:
            return self.mod2.try_select(board, square)

    def wait_action(self, board):
        if not self.mod1.ended:
            return self.mod1.wait_action(board)
        else:
            return self.mod2.wait_action(board)

    def on_exit(self):
        # TODO exit modul 1 early? e.g. quit engines and stuff
        self.mod1.on_exit()
        self.mod2.on_exit()


class ModuleProduct3(GameModule):
    """Join three modules, the first one has to end, then the second

    This can be achieved compositionally with two regular
    `ModuleProduct`, but I like it this way :D

    """
    def __init__(self, mod1, mod2, mod3):
        self.mod1 = mod1()
        self.mod2 = mod2()
        self.mod3 = mod3()

    def try_move(self, board, source_sq, target_sq) -> bool:
        if not self.mod1.ended:
            return self.mod1.try_move(board, source_sq, target_sq)
        elif not self.mod2.ended:
            return self.mod2.try_move(board, source_sq, target_sq)
        else:
            return self.mod3.try_move(board, source_sq, target_sq)
        
    def try_select(self, board, square):
        if not self.mod1.ended:
            return self.mod1.try_select(board, square)
        elif not self.mod2.ended:
            return self.mod2.try_select(board, square)
        else:
            return self.mod3.try_select(board, square)

    def wait_action(self, board):
        if not self.mod1.ended:
            return self.mod1.wait_action(board)
        elif not self.mod2.ended:
            return self.mod2.wait_action(board)
        else:
            return self.mod3.wait_action(board)

    def on_exit(self):
        # TODO exit modul 1 early? e.g. quit engines and stuff
        self.mod1.on_exit()
        self.mod2.on_exit()
        self.mod3.on_exit()
    
        
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

        return result 

    def opponent_move(self, board):
        raise Exception("Function not defined in PvE module: `opponent_move`.")
    def wait_action(self, board):
        # If it's the turn of the opponent, do the move. 
        if board.turn != self.player_color:
            self.opponent_move(board)
        
    def try_select(self, board, square):
        # If it's not your turn you can't select
        if board.turn != self.player_color:
            return False
        # If it is your turn, try to select in the normal way
        return PvP.try_select(self,board,square)
    
