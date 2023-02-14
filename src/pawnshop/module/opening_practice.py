import chess
import chess.pgn as PGN
import module.module as M
import random
import debug.debug as DB
import os
import menu

class OpeningPracticeModule(M.PvE, M.ModuleEnds):
    """Opening Practice

    This engine takes a pgn file as input, with opening prep. It then
    "quizes" the player by following the prep tree.
    """
    name = "Opening Practice"
    def __init__(self):
        M.PvE.__init__(self)
        M.ModuleEnds.__init__(self) # creates self.ended
        self.current_game = None
        # Get Prep files:
        
        self.folder_path = "prep/" # replace with the actual folder path
        pgn_files = [f for f in os.listdir(self.folder_path) if f.endswith('.pgn')]

        self.prep_names = [os.path.splitext(pgn_file)[0] for pgn_file in pgn_files]
        print("Preps: ", self.prep_names)
        
        #Default
        self.prep_name = self.prep_names[0]
        
    def opponent_move(self):
        if self.ended:
            return False
        # Check that the game and the prep are synced
        if self.board.turn != self.current_game.turn():
            raise Exeption("board and prep got out of sync!")
        
        # Get the possible next moves and check it's not empty
        variations = self.current_game.variations
        if variations:
            next_game = random.choice(variations)
            self.board.push(next_game.move)
            self.current_game = next_game
        else:
            self.ended = True
            DB.debug(2, "End of prep.")
            return False

    def try_move(self, source_sq, target_sq) -> bool:
        if self.ended:
            return False
        
        if source_sq < 0:
            return False

        self.status = ""
        move = chess.Move(source_sq, target_sq)
        # For now we only support promoting to queen (automatically)
        move_promo = chess.Move(source_sq, target_sq, chess.QUEEN)
        
        # The check if the move is in the prep
        variations = self.current_game.variations
        if not variations:
            self.ended = True
            print ("Opening Ended")
            return False
            
        prep_moves = [game.move for game in variations]
        if move in prep_moves:
            index = prep_moves.index(move)
        elif move_promo in prep_moves:
            index = prep_movedones.index(move_promodone)
        else:
            if self.board.is_legal(move):
                print("STR: ", str)
                self.status = str(move) + " is not in your prep."
            return False
        
        self.current_game = variations[index]
        self.board.push(self.current_game.move)
        return True

    #####################
    # Configuration menue
    #####################
    def get_config_menu(self):
        config_menu = M.PvE.get_config_menu(self)
        choose_prep_label = menu.mk_label("Choose Prep")
        choose_prep = menu.mk_drop_down(self.set_prep, self.prep_names, self.prep_names[0])
        return config_menu + [choose_prep_label, choose_prep]
        
    def set_prep(self, prep_file):
        self.prep_name = prep_file

    def update_config(self):
        super().update_config()
        prep_file = open("prep/"+self.prep_name+".pgn")
        full_prep = PGN.read_game(prep_file)
        self.current_game = full_prep
