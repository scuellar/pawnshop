""" Modules are pluggins for PawnShop, they can implement different ways to play the game:

Examples:
- Local PvP
- Against an engine
- Practice openings
- Play online (through lichess)

"""
import chess
from typing import Optional

################
# Game Modules
################

class GameModule:
    name = "Game Module"
    status = ""
    
    def __init__(self, board = chess.Board()):
        self.board = board
        self.config_menu = []
        
    def try_move(self, source_sq, target_sq) -> bool:
        raise Exception("Function not defined in Game Module: `try_move`.")
    
    def try_select(self, square):
        raise Exception("Function not defined in Game Module: `try_select`.")

    def wait_action(self):
        """ What to do when no action has been triggered.
        """
        pass

    def on_exit(self):
        pass

    # Basic interface
    
    def get_name(self):
        return self.name
    
    def get_status(self):
        return self.status
    
    def piece_at(self, square):
        return self.board.piece_at(square)

    def last_move(self) -> Optional[chess.Move]:
        if self.board.move_stack:
            return self.board.peek()
        else:
            return None

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
        GameModule.__init__(self)
        self.mod1 = mod1()
        self.mod2 = mod2()
        self.mod1.set_board(self.board)
        self.mod2.set_board(self.board)

    def set_board(self, board):
        self.board = board
        self.mod1.set_board(self.board)
        self.mod2.set_board(self.board)
        

    def try_move(self, source_sq, target_sq) -> bool:
        if not self.mod1.ended:
            return self.mod1.try_move(source_sq, target_sq)
        else:
            return self.mod2.try_move(source_sq, target_sq)
        
    def try_select(self, square):
        if not self.mod1.ended:
            return self.mod1.try_select(square)
        else:
            return self.mod2.try_select(square)

    def wait_action(self):
        if not self.mod1.ended:
            return self.mod1.wait_action()
        else:
            return self.mod2.wait_action()

    def on_exit(self):
        # TODO exit modul 1 early? e.g. quit engines and stuff
        self.mod1.on_exit()
        self.mod2.on_exit()

    name =  "Product"
    def get_name(self):
        if not self.mod1.ended:
            in_name = self.mod1.get_name()
        else:
            in_name = self.mod2.get_name()
        return self.name + ", " + in_name
        
    def get_status(self):
        if not self.mod1.ended:
            return self.mod1.get_status()
        else:
            return self.mod2.get_status()


class ModuleProduct3(ModuleProduct):
    """Join three modules, the first one has to end, then the second

    This can be achieved compositionally with two regular
    `ModuleProduct`, but I like it this way :D

    """
    def __init__(self, mod1, mod2, mod3):
        GameModule.__init__(self)
        self.mod1 = mod1()
        self.mod2 = ModuleProduct(mod2, mod3)

        self.mod1.set_board(self.board)
        self.mod2.set_board(self.board)

    name =  "Product3"
    def get_name(self):
        """
        We overrride this function so it doesn't stack the Product's.
        If we don't, it would say (e.g.) "(Product3, Product, mod1)"
        """
        if not self.mod1.ended:
            in_name = self.mod1.get_name()
        elif not self.mod2.mod1.ended:
            in_name = self.mod2.mod1.get_name()
        else:
            in_name = self.mod2.mod2.get_name()
        return self.name + ", " + in_name
    
        
####################
# Some basic modules
####################

# + Local Player vs. Player
class PvP(GameModule):
    """ Player vs. Player
    The basic module to play locally on the same screen
    """
    name = "PvP"
    def __init__(self):
        GameModule.__init__(self)

    def set_board(self, board):
        """Changes the board. Usefull for composition.

        Any module that caries aditional state should problaly
        redefine this function, to reset the state.
        """
        self.board = board
        return True

        
    def try_move(self, source_sq, target_sq) -> bool:
        if source_sq >= 0:
            move = chess.Move(source_sq, target_sq)
            # For now we only support promoting to queen (automatically)
            move_promo = chess.Move(source_sq, target_sq, chess.QUEEN)
            if self.board.is_legal(move):
                self.board.push(move)
                return True
            elif self.board.is_legal(move_promo):
                self.board.push(move_promo)
                return True
            else:
                print ("Not a legal move", move)
        return False

    def try_select(self, square):
        if self.board.piece_at(square):
            if self.board.piece_at(square).color == self.board.turn:
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
    name = "PvE"
    def __init__(self):
        PvP.__init__(self)
        self.player_color = chess.WHITE
    
    def change_side(self):
        if self.can_change_sides:
            if self.player_color == chess.WHITE:
                self.player_color = chess.BLACK
            else:
                self.player_color = chess.WHITE
        
    def try_move(self, source_sq, target_sq) -> bool:
        # If it's not your turn you cna't move
        if self.board.turn != self.player_color:
            return False

        # If it is your turn, try to move in the normal way
        result = PvP.try_move(self, source_sq, target_sq)

        return result 

    def opponent_move(self):
        raise Exception("Function not defined in PvE module: `opponent_move`.")
    
    def wait_action(self):
        # If it's the turn of the opponent, do the move. 
        if self.board.turn != self.player_color:
            self.opponent_move()
        
    def try_select(self, square):
        # If it's not your turn you can't select
        if self.board.turn != self.player_color:
            return False
        # If it is your turn, try to select in the normal way
        return PvP.try_select(self, square)
