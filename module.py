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

################
# Local Player vs. Player
################
class PvP(GameModule):
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
    

