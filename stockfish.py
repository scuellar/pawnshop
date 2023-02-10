import chess
import chess.engine
import module as M

class StockfishModule(M.PvE):
    """StockfishModule

    This engine just runs stockfish in the background
    """
    def __init__(self):
        M.PvE.__init__(self)
        self.engine = chess.engine.SimpleEngine.popen_uci(r"/usr/local/bin/stockfish")
        self.time_limit = 0.1 # 100 milliseconds per move

    def opponent_move(self, board):
        # Get the possible next moves and check it's not empty
        result = self.engine.play(board, chess.engine.Limit(time=0.1))
        print("Oponent move:", result.move)
        board.push(result.move)

    def on_exit(self):
        self.engine.quit()
    
# pgn_file = open("prep/dragon.pgn")
# dragon = PGN.read_game(pgn_file)

# for move in dragon.mainline_moves():
#     print(move)

# print("----")
# print("Variations:", len(dragon.variations))
