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


class EverymanModule(M.PvE):
    """Every Man is a module that plays like the average lichess player
 
    In each position, this engine checks evey move that has been
    played by lichess players and whith what frequency. Using those
    numbers as a distribuition over responses, this engin randomly
    chooses the next move.
    """
    def __init__(self):
        M.PvE.__init__(self)
        self.history = []
        
        self.opening_ended = False
        """ Flipped when you reach a game never seen before in the database."""
        
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
        if self.opening_ended:
            return False
        last_move = board.peek()
        self.history = self.history + [last_move.uci()] 
        next_move_uci = self.choose_next_move(board)
        if next_move_uci == None:
            print("OPENING ENDED!!!")
            print("End history:", self.history)
            self.opening_ended = True
            return False
        next_move = chess.Move.from_uci(next_move_uci)
        self.history = self.history + [next_move.uci()] 
        board.push(next_move)
