import module as M
import random
import chess
import lichessTalk as lt
# import asyncio

def unzip(ls):
    print("The list", ls)
    l1 = [i for (i,j) in ls]
    l2 = [j for (i,j) in ls]
    return (l1,l2)


class EverymanModule(M.PvP):
    def __init__(self):
        self.player_color = chess.WHITE
        self.history = []

    def choose_next_move(self, board):
        play = ",".join(self.history)
        print("Play so far: ", play)
        dist = lt.get_distribution(play)
        if len(dist)==0:
            return None
        (moves,count) = unzip(dist)

        next_move = random.choices(moves, count)
        print ("Next move", next_move)
        return next_move[0]

    def opponent_move(self, board):
        last_move = board.peek()
        self.history = self.history + [last_move.uci()] 
        next_move_uci = self.choose_next_move(board)
        if next_move_uci == None:
            print("OPENING ENDED!!!")
            return False
        next_move = chess.Move.from_uci(next_move_uci)
        self.history = self.history + [next_move.uci()] 
        board.push(next_move)
        
    def try_move(self, board, source_sq, target_sq) -> bool:
        if board.turn != self.player_color:
            return False

        result = M.PvP.try_move(self, board, source_sq, target_sq)

        if result:
            self.opponent_move(board)
        return result 
        
    def try_select(self, board, square):
        if board.turn != self.player_color:
            return False
        return M.PvP.try_select(self,board,square)
