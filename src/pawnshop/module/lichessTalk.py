import lichess.openings as Opening
import debug.debug as DB

# Some ad-hoc setting
max_moves = 20 # the possible moves in the first turn.
init_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

def simpl_move (move):
    uci = move['uci']
    (white, draw, black) = (move['white'],move['draws'],move['black'])
    total = white+draw+black
    return (uci, total)

def get_distribution(play, fen = init_fen, moves = max_moves):
    ops = Opening.openings_lichess(fen, play = play, topGames = 0, moves = moves)
    opening_name = ops['opening']['name']
    DB.debug(2, "Current opening", opening_name)
    return (opening_name, [ simpl_move(move) for move in ops['moves'] ])
