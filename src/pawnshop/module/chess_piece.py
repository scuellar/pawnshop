import pygame.midi
from pawnshop.module import module as M
import chess
import chess.pgn as PGN
from time import sleep
import os
from pawnshop import menu
import mido

scale_incr = [0,2,4,5,7,9,11]
scale = []
for base in range(5):
    note_base = (60-24) + base*12
    scale = scale + [note_base + incr for incr in scale_incr]  
#scale = [60, 62, 64, 65, 67, 69, 71, 72]


class ChessPiece(M.GameModule, M.ModuleEnds):
    name = "Game Module"
    status = ""
    
    def __init__(self, board = chess.Board()):
        M.GameModule.__init__(self)
        self.cache_notes = []
        self.game_name = ""

        ### init the midi stuff
        pygame.midi.init()

    
        # print("PORT number", pygame.midi.get_count)
        # for n in range(pygame.midi.get_count()):
        #     print("DEVICE:",pygame.midi.get_device_info(n))

        # print("Default:", pygame.midi.get_default_output_id())
            
        self.playerW = pygame.midi.Output(3)
        self.playerB = pygame.midi.Output(4)
        self.playerW.set_instrument(0)
        self.playerB.set_instrument(1)
        
        self.velocity = 127  # The velocity (0-127)
        self.step = 400
        
        # Get game files:
        
        self.folder_path = "musical_games/" # replace with the actual folder path
        pgn_files = [f for f in os.listdir(self.folder_path) if f.endswith('.pgn')]

        self.game_names = [os.path.splitext(pgn_file)[0] for pgn_file in pgn_files]
        print("games: ", self.game_names)
        
        self.ended = False
        

    def try_move(self, source_sq, target_sq) -> bool:
        return False #This game just plays music
    
    def try_select(self, square):
        return False #This game just plays music
    
    def wait_action(self):
        """ Now we play the music.
        """
        print("started")
        if self.ended:
            return False
        
        # Check that the game and the prep are synced
        # if self.board.turn != self.current_game.turn():
        #     print("board and prep got out of sync!")
        #     raise Exeption("board and prep got out of sync!")

        if self.current_game.is_end():
            self.ended = True
            return False
        
        print("Pass checks")
        # Get the possible next moves and check it's not empty
    
        move = self.current_game.move
        print("got move", move)
        self.current_game = self.current_game.next()
        
        print("Got move and next game")
        if move:
            from_sq = move.from_square
            piece = self.board.piece_at(from_sq)
            turn = self.board.turn
            self.board.push(move)

            notes = self.cache_notes
            self.cache_notes, velocity = self.choose_note(move, piece, turn) 

            if self.board.turn == chess.WHITE:
                player = self.playerW
            else:
                player = self.playerB
                
        
            for (note,duration) in notes:
                player.note_on(note, self.velocity)
                pygame.time.wait(duration)  # Wait for half a second
                player.note_off(note)
            
        
    def on_exit(self):
        del self.playerW  # Release the MIDI device
        del self.playerB  # Release the MIDI device
        pygame.midi.quit()

    
    #####################
    # Configuration menue
    #####################
    def get_config_menu(self):
        config_menu = []
        choose_game_label = menu.mk_label("Choose game")
        choose_game = menu.mk_drop_down("Choose game", self.set_game, self.game_names, self.game_names[0])
        return config_menu + [choose_game]
        
    def set_game(self, game_file):
        self.game_name = game_file

    def update_config(self):
        if self.game_name=="":
            self.game_name = self.game_names[0]
        print("current game: ", self.game_name)
        super().update_config()
        game_file = open(self.folder_path+self.game_name+".pgn")
        full_game = PGN.read_game(game_file)
        self.current_game = full_game
        print("Full game:", full_game)

        
    def choose_note(self, move, piece, color):
            return self.choose_note_piece(move,piece, color)

    def choose_note_piece(self, move, piece, color):
        from_sq = move.from_square
        from_file = chess.square_file(from_sq)
        from_rank = chess.square_rank(from_sq)
        to_sq = move.to_square
        to_file = chess.square_file(to_sq)
        to_rank = chess.square_rank(to_sq)

        # move forward?
        if color == chess.WHITE:
            forward = (from_rank < to_rank)
        else:
            forward = (from_rank > to_rank)
        
        oct1 = 0
        oct2 = 7
        oct3 = 14
        oct4 = 21
        
        notes = []
        step = self.step
        
        # Modify based on piece
        print("piece type", type(piece), piece)
        if piece.piece_type == chess.PAWN:
            notes = [(scale[oct4+to_rank],step//2)]
        elif piece.piece_type == chess.ROOK:
            notes = [(scale[oct1+to_rank],step*2)]
        elif piece.piece_type == chess.KNIGHT:
            notes = [(scale[oct3+to_rank],step)]
        elif piece.piece_type == chess.BISHOP:
            notes = [(scale[oct3+to_rank],step//2)]*2
        elif piece.piece_type == chess.QUEEN:
            notes = [(scale[oct2+to_rank],step),(scale[oct2+to_rank+1],step)]
        elif piece.piece_type == chess.KING:
            notes = [(scale[oct2+to_rank],step)]*2

        print("Piece", piece, " From:", from_sq, " to ", to_sq, ". NOTES", notes)
        return (notes, self.velocity)
    
        
    def choose_note_rank(self, move, piece, color):
        from_sq = move.from_square
        from_file = chess.square_file(from_sq)
        from_rank = chess.square_rank(from_sq)
        to_sq = move.to_square
        to_file = chess.square_file(to_sq)
        to_rank = chess.square_rank(to_sq)
        piece = self.board.piece_at(from_sq)

        bn = scale[14+to_rank] # Base note
        bn_1 = scale[14+to_rank+1] # Base note
        bn_2 = scale[14+to_rank+1] # Base note
        
        
        notes = []
        step = self.step
        
        # Modify based on piece
        print("piece type", type(piece), piece)
        if piece.piece_type == chess.PAWN:
            notes = [(bn, step//2),(0, step//2)]
        elif piece.piece_type == chess.ROOK:
            notes = [(bn, step//2)]*4
        elif piece.piece_type == chess.KNIGHT:
            notes = [(bn, 2*step//3),(bn_1,step//2)]
        elif piece.piece_type == chess.BISHOP:
            notes = [(bn, step//3),(bn_1,step//3),(bn, step//3)]
        elif piece.piece_type == chess.QUEEN:
            notes = [(bn, step//2),(bn_1,step//2),(bn_2, step//2),(bn, step//2)]
        elif piece.piece_type == chess.KING:
            notes = [(bn, 2*step)]
            

        
        print("Piece", piece, " From:", from_sq, " to ", to_sq, ". NOTES", notes)
        return (notes, self.velocity)
        
