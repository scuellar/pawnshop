import lichess.openings as Opening

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
    return ([ simpl_move(move) for move in ops['moves'] ])
    
# op = Opening.openings_lichess("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", play = "e2e4,e7e5", since = "2022-01", topGames = 0, moves = 20)

# ucis = [move['uci'] for move in op['moves']]
# print("Moves", len(ucis))

dist = get_distribution("e2e4,e7e5")
