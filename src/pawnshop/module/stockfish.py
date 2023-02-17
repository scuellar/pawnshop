import chess
import chess.engine
import module.module as M

class StockfishModule(M.PvE):
    """StockfishModule

    This engine just runs stockfish in the background
    """
    name = "stockfish"
    def __init__(self):
        M.PvE.__init__(self)
        self.engine = chess.engine.SimpleEngine.popen_uci(r"/usr/local/bin/stockfish")
        self.time_limit = 0.1 # 100 milliseconds per move

    def opponent_move(self):
        # Get the possible next moves and check it's not empty
        result = self.engine.play(self.board, chess.engine.Limit(time=0.1))
        print("Oponent move:", result.move)
        self.board.push(result.move)

    def on_exit(self):
        print("Exiting Engine")
        self.engine.quit()
    
# pgn_file = open("prep/dragon.pgn")
# dragon = PGN.read_game(pgn_file)

# for move in dragon.mainline_moves():
#     print(move)

# print("----")
# print("Variations:", len(dragon.variations))
