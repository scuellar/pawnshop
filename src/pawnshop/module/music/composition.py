import pygame
import pygame.midi
from random import choice
from checkers import *
from time import sleep
import cProfile

def lead_speed():
    return choice([1,1,1,2,2,3])
step = 900

def flat_list(lss):
    return [item for sublist in lss for item in sublist]
        
class MelodicStep():
    """ Corresponds to a search step of the melody
    """
    def init_stats(self):
        if self.stats_lead and self.stats_cantus:
            return
        
        if self.parent:
            self.stats_lead   = self.parent.stats_lead.ExtendStats(self.lead[0])
            self.stats_cantus = self.parent.stats_cantus.ExtendStats(self.cantus)
        else:
            self.stats_lead   = MelodyStats()
            self.stats_lead.add_notes(self.lead[0])
            self.stats_cantus = MelodyStats()
            self.stats_cantus.add_notes(self.cantus)
            
    def __init__(self, lead_step, cantus_step, parent=None, name = "Root"):
        if parent:
            self.depth = parent.depth + 1
        else:
            self.depth = 0
        self.stats_lead   = None
        self.stats_cantus = None
        self.lead_speed = lead_speed()
        self.parent = parent
        self.lead   = lead_step      # next lead notes
        self.cantus  = cantus_step   # next cantus notes
        self.next_notes  = []
        self.current  = None    # the currently explored one
        if parent:
            self.past_melody = self.parent.get_melody()
        else:
            self.past_melody = ([],[])
        #self.extra_info = extra_info

        self.name = name
        self.searched_branches = 0
        

    def get_melody(self):
        # TODO cache this melody
        past_lead, past_cantus = self.past_melody
        #print("======= Getting melody for ", self.name)
        self.init_stats()
        #print("STATS:", self.stats_lead.melody)
        #print("MELODY", past_lead + self.lead)
        return (past_lead + self.lead, past_cantus + self.cantus)

    #########
    # Checks
    #########

    def check_melody(self, notes, type, verbose = False):
        """ Check local properties to see if melody is good so far
        """
        # past_lead, past_cantus = self.get_melody()
        if not self.stats_cantus:
            self.init_stats()
            
        if type == 'cantus':
            stats = self.stats_cantus
        elif type == 'lead':
            stats = self.stats_lead
        return check_melody_idependent(stats, type, verbose)

    def check_harmony(self, notes, cnotes, verbose = True):
        cantus = self.cantus + cnotes
        leads   = self.lead +   [notes]
        # We only check harmony with the active beat
        lead = [notes[0] for notes in leads]
        return check_harmony_independent(lead, cantus, verbose)
    
    def check_globals(self, verbose=False):
        """ Check global properties that cna only be checked once the phrase is over
        """
        lead, cantus = self.get_melody()
        lead_flat = flat_list(lead)
        return check_globals_independent(cantus, verbose) and check_globals_independent(lead_flat, verbose)

    #########
    # filters
    #########
    def filter_cantus(self, notes, verbose):
        """ Quick checks for the cantus
        """
        notes = [n for n in notes if self.check_melody([n], 'cantus', verbose)]
            
        return notes # for now, don't filter anything
        
    def filter_lead(self, notes_list, cnote, verbose):
        """ Quick checks for the lead
        """
        # Check as melody
        notes_list = [ns for ns in notes_list if self.check_melody(ns, 'lead', verbose)]
        # Check harmony
        notes_list = [ns for ns in notes_list if self.check_harmony(ns, [cnote], verbose)]
        
        return notes_list # for now, don't filter anything
        

    def get_next_leads(self, last_vn, last_cn, count, register, head=[]):
        allowed_intervals = [Unison, m2, M2, M3, P4, P5, m6]
        allowed_vertical_intervals = [m3, M3, P5, m6, M6]
        available_notes = [x for x in register if abs(x - last_vn) in allowed_intervals
			   and x > last_cn # no cross-over
			   and abs(x - last_cn) < (P8 + P5) # no vertical interval larger than 12th
			   ]
        if not head: # Only if it's the first, accented beat
            available_notes = [x for x in available_notes
                               if abs(x - last_cn) % Octave in allowed_vertical_intervals # consonant vertical interval
                               ]
        # only care about the ones in our register (intersection)
        vnotes = list(set(available_notes) & set(register))
        ## Filter
        vnotes_list = [head + [vn] for vn in vnotes]
        vnotes_list = self.filter_lead(vnotes_list, last_cn, verbose)
        if count == 1:
            return vnotes_list
        next_lead = [] 
        for vns in vnotes_list:
            more_vnotes = self.get_next_leads(vns[-1], last_cn, count-1, register, head = vns)
            next_lead = next_lead + more_vnotes
        return next_lead
        
    def search_next(self, register, verbose = False):
        #print("search_next")
        """ Finds all possible next steps
        """
        next_notes = []
        cur_lead, cur_cantus = self.get_melody()
        #####################
        # Search for a cantus
        #####################
        allowed_intervals = [m2, M2, M3, P4, P5, m6]
        # next note can go up or down.
        cnotes_up   = [cur_cantus[-1] + n for n in allowed_intervals]
        cnotes_down = [cur_cantus[-1] - n for n in allowed_intervals]
        cnotes = cnotes_up + cnotes_down
        # only in the register
        cnotes = list(set(cnotes) & set(register))
        cnotes = self.filter_cantus(cnotes, verbose)
        #print("================ FOUND NEXT CNOTES")
        #print("CNOTES:", cnotes)
        #####################
        # Search for a leading voice
        #####################
        #print("search_next got some cnotes:", cnotes)
        for cnote in cnotes:
        # next note can go up or down or equal.
            last_vn = cur_lead[-1][-1]
            vnotes = self.get_next_leads(last_vn, cnote, self.lead_speed, register)
            # print("LEAD notes", vnotes)
            # TODO Duplicated work!
            
            #print("For cnote:", cnote, "Found a leads", vnotes)
            vnotes = self.filter_lead(vnotes, cnote, verbose)
            more_next_notes = [(vn, cnote) for vn in vnotes]
            next_notes = next_notes + more_next_notes

        #print("and we are done")
        if next_notes:
            #print("yes we are. With next notes", next_notes)
            #self.next_notes = [MelodicStep([lnote], [cnote], self) for (lnote, cnote) in next_notes]
            self.next_notes = next_notes
            #print("we even returned!")
            return True
        else:
            #print("no we are not")
            return False

    def choose_next_note(self, verbose = False):
        #print("choose_next_note")
        """ From all the possible next steps, it chooses one, using heuristics.
        """

        # First compute next notes 
        if not self.next_notes and not self.current:
            #print("I got to pick some ")
            if not self.search_next(Mreg, verbose):
                return False

        #print("choose_next_note got next notes")
        
        if self.next_notes:
            
            #print("choose_next_note HAS next notes")
            lnote, cnote = self.next_notes[0]
            child_name = self.name + "-" + str(self.searched_branches)
            self.current =  MelodicStep([lnote], [cnote], self, name=child_name)
            self.searched_branches = self.searched_branches + 1
            self.next_notes = self.next_notes[1:]
        else:
            #print("choose_next_note DOESNT HAVE  next notes")
            ### If after computing notes, it's empty that means there is
            ### no viable branch or we explored them all
            if verbose: print("Ran out of branches to explore. Backtrack!")
            return False

        return True

LENGTH  = 10
   
class PhraseSearch():
    """Object made to search a phrase
    """

    ############
    # TODO: Keep stats (intervals, leasp) as a running list
    # to reduce recomputation
    ############
    
    def __init__(self, length = LENGTH, verbose = False):
        self.length = length

        #### Get the first node on the search
        initial_lead = choice ([I,III,V,P8])
        self.base = MelodicStep([[initial_lead]],[I]) # Root search node
        self.current = self.base                           # Current search node

    def search_next(self):
        #print("search_next")
        if self.current.choose_next_note(verbose = verbose):
            current = self.current.current
            if verbose: self.print_melody()
            return current
        else:
            #print("nothing found")
            return None

    def find(self):
        """ Find the phrase
        """
        
        while True:
            #print("find step")
            proposed_next = self.current
            while proposed_next:
                #print("next step1")
                self.current = proposed_next
                depth = self.current.depth
                # Check if it's done
                if depth+1 >= self.length:
                    # Check if it's a good melody
                    if self.current.check_globals():
                        print("DONE!")
                        return True
                    else:
                        #print("Globally failed")
                        break
                #print("Did the checks")
                proposed_next = self.search_next()
                #self.print_melody()
                #sleep(1)
                #x = input()
            ### BACKTRACK
            # If the loop breaks, it found a bad melody
            self.current = self.current.parent
            if not self.current:
                # Backtracked all the way to the root
                # No melodies found
                print ("Completly failed!")
                return False

        
    def get_melody(self):
        """ Gets the current best melody.
        When search is completed, this returns the chosen melody
        """
        return self.current.get_melody()
    
    def print_melody(self):
        lead, cantus = self.get_melody()
        def print_ls(ls):
            ret = ""
            for x in ls:
                s = str(x)
                padd_len = 3 - len(s)
                padd = " " * padd_len
                ret = ret + s + padd
            return ret
        lead_str = [print_ls(ls) for ls in lead]
        for ln in lead_str:
            print(ln, end="")
        print("")
        for i, cn in enumerate(cantus):
            padd_len = len(lead_str[i]) - len(str(cn))
            padd = " " * padd_len
            print(cn, end=padd)
        print("")
        


### Test

verbose = False # True
    
def quit(players):
    for player in players:
        del player  # Release the MIDI device
    pygame.midi.quit()
    pygame.quit()
    exit()


velocity = 127  # The velocity (0-127)



def play(melody , players=[]):
    global current
    global length
    global step
    global velocity

    # Init
    if not players: 
        pygame.init()
        pygame.midi.init()
    
        if verbose:
            print("PORT number", pygame.midi.get_count)
            for n in range(pygame.midi.get_count()):
                print("DEVICE:",pygame.midi.get_device_info(n))
        
        #print("Default:", pygame.midi.get_default_output_id())
        player1 = pygame.midi.Output(3)
        player1.set_instrument(0)
        player2 = pygame.midi.Output(4)
        player2.set_instrument(1)
    elif len(players)==2:
        player1,player2=players
    else:
        print ("Wrong number of players")
        quit(players)
        return

    # Play
    lead, cantus = melody
    for (ls,c) in zip(lead, cantus):
        count = len(ls)
        player2.note_on(c+60, velocity)
        for l in ls:
            player1.note_on(l+60, velocity)
            pygame.time.wait(600//count)  # Wait for half a second
            player1.note_off(l+60)
        player2.note_off(c+60)

    return ([player1, player2])

def run(count=10, stop=True, should_play=True):
    players = []
    phrase_count = 3
    melodies = []
    
    for i in range(count):
        melodies = []
        for i in range(phrase_count):
            print("========= Generating Phrase", i, "========")
            phrase = PhraseSearch()
            if phrase.find():
                melodies = [phrase.get_melody()] + melodies
                phrase.print_melody()

        if should_play:
            print("========= Playing the music ========")
            for i, melody in enumerate(melodies):
                print(i, "...", end="")
                players = play(melody,players)
            print("Done")

        if stop:
            x = input()
            if x in ["quit","exit","quit()","exit()","q"] :
                break

    if should_play:
        quit(players)

def profile_run():
    run(count=10,stop=False, should_play=False)
    
    
stats_file = 'runstats_funcs_out'
cProfile.run('profile_run()', stats_file)

import pstats
from pstats import SortKey
p = pstats.Stats(stats_file)
p.strip_dirs().sort_stats(SortKey.TIME, SortKey.CUMULATIVE).print_stats(20)
    
# run()
