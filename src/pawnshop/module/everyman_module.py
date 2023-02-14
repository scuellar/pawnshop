import module.module as M
import random
import chess
import module.lichessTalk as lt
# import asyncio

def unzip(ls):
    print("The list", ls)
    l1 = [i for (i,j) in ls]
    l2 = [j for (i,j) in ls]
    return (l1,l2)


class EverymanModule(M.PvE, M.ModuleEnds):
    """Every Man is a module that plays like the average lichess player
 
    In each position, this engine checks evey move that has been
    played by lichess players and whith what frequency. Using those
    numbers as a distribuition over responses, this engin randomly
    chooses the next move.
    """
    name = "average chess"
    def __init__(self):
        M.PvE.__init__(self)
        M.ModuleEnds.__init__(self) # Creates self.ended = False

    
        self.ended = False
        """ Flipped when you reach a game never seen before in the database."""
    def history(self):
        # Create the history from the board.  If this module is
        # stand-alone, it will be empty, but this could follow from a
        # initial game or a playing with a previous module
        history = [move.uci() for move in self.board.move_stack]
        print("EMModule: Here are the moves so far", history)
        return history #TODO can we cache?
        
    def choose_next_move(self):
        play = ",".join(self.history())
        print("Play so far: ", play)
        dist = lt.get_distribution(play)
        if len(dist)==0:
            return None
        (moves,count) = unzip(dist)

        next_move = random.choices(moves, count)
        print ("Next move", next_move)
        return next_move[0]

    def opponent_move(self):
        if self.ended:
            return False
        last_move = self.board.peek()
        next_move_uci = self.choose_next_move()
        if next_move_uci == None:
            print("OPENING ENDED!!!")
            print("End history:", self.history())
            self.ended = True
            return False
        next_move = chess.Move.from_uci(next_move_uci)
        self.board.push(next_move)
