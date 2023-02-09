import chess
import chess.pgn as PGN
import module as M
import random

class OpeningPracticeModule(M.PvE):
    """Opening Practice

    This engine takes a pgn file as input, with opening prep. It then
    "quizes" the player by following the prep tree.
    """
    def __init__(self):
        M.PvE.__init__(self)
        self.opening_ended = False
        
        pgn_file = open("prep/dragon.pgn")
        self.full_prep = PGN.read_game(pgn_file)
        print("Hey, I loaded a game:", self.full_prep)
        self.current_game = self.full_prep

    def opponent_move(self, board):
        if self.opening_ended:
            return False
        # Check that the game and the prep are synced
        if board.turn != self.current_game.turn():
            raise Exeption("board and prep got out of sync!")
        
        # Get the possible next moves and check it's not empty
        variations = self.current_game.variations
        if variations:
            next_game = random.choice(variations)
            board.push(next_game.move)
            self.current_game = next_game
        else:
            self.opening_ended = True
            print ("Opening Ended")
            return False

    def try_move(self, board, source_sq, target_sq) -> bool:
        if self.opening_ended:
            return False
        
        if source_sq < 0:
            return False
        
        move = chess.Move(source_sq, target_sq)
        # For now we only support promoting to queen (automatically)
        move_promo = chess.Move(source_sq, target_sq, chess.QUEEN)
        
        # The check if the move is in the prep
        variations = self.current_game.variations
        if not variations:
            self.opening_ended = True
            print ("Opening Ended")
            return False
            
        prep_moves = [game.move for game in variations]
        if move in prep_moves:
            index = prep_moves.index(move)
        elif move_promo in prep_moves:
            index = prep_movedones.index(move_promodone)
        else:
            return False
        
        self.current_game = variations[index]
        board.push(self.current_game.move)
        return True
        
# pgn_file = open("prep/dragon.pgn")
# dragon = PGN.read_game(pgn_file)

# for move in dragon.mainline_moves():
#     print(move)

# print("----")
# print("Variations:", len(dragon.variations))
