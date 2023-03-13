import math

def sign(x):
    return math.copysign(1, x)

def remove_dupes(ls):
    return [*set(ls)]

# Constants for convenience

KEY_NAMES = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
KEY_NAMES_SHARP = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

P1 = C  = I   = Tonic = Unison = 0
m2 = Db = ii                = 1
M2 = D  = II  = Step        = 2
m3 = Eb = iii               = 3
M3 = E  = III               = 4
P4 = F  = IV                = 5
d5 = Gb = Vo  = Tritone     = 6
P5 = G  = V                 = 7
m6 = Ab = vi                = 8
M6 = A  = VI                = 9
m7 = Bb = vii               = 10
M7 = Bb = VII = LeadingTone = 11
P8      = O   = Octave      = 12

registers = {
    'major': [IV-O, V-O, VI-O, VII-O, I, II, III, IV, V, VI, VII, I+O, II+O, III+O, IV+O],
    'minor': [IV-O, V-O, vi-O, vii-O, I, II, iii, IV, V, vi, vii, I+O, II+O, iii+O, IV+O]
}
Mreg = registers['major']
mreg = registers['minor']

verbose = False
verbose0 = True

#### CHECKERS
def get_runs_from_melody(melody):
    # e.g.
    # 	input: [0, 2, 4, 2, 0, 7, 5, -3, 2, 0]
    #	output: [[0, 2, 4], [4, 2, 0], [7, 5, -3]]

    runs = []
                                       
    for i in range(len(melody) - 2):
        for j in range(i + 2, len(melody)):
            trial_run = melody[i:j+1]
            directions = [sign(trial_run[i+1] - trial_run[i]) for i in range(len(trial_run) - 1)]
            all_directions_equal = (directions.count(directions[0]) == len(directions))
            if all_directions_equal:
                runs.append(tuple(trial_run))
    runs = remove_dupes(runs)

    # remove runs contained in other runs

    contained_runs = []
    for run1 in runs:
        for run2 in runs:
            if run1 != run2 and ''.join(map(str, run2)) in ''.join(map(str, run1)): # run2 contained in run1
                if run2 not in contained_runs:
                    contained_runs.append(run2)

    for run in contained_runs:
        runs.remove(run)

    return runs

class MelodyStats():
    """ Keeps stats of the melody including:
    intervals
    directions
    leaps
    notes
    """
    def __init__(self):
        self.length     = 0
        self.melody     = []
        self.intervals  = []
        self.directions = []
        self.leaps      = []
        self.notes      = []

    def add_notes(self, new_notes):
        self.length = self.length + len(new_notes)
        tail = self.melody[-1:] + new_notes
        new_intervals  = [tail[i+1] - tail[i] for i in range(len(tail) - 1)]
        
        self.melody     += new_notes
        self.intervals  += new_intervals
        self.directions += [sign(new_intervals[i]) for i in range(len(new_intervals))]
        self.leaps      += [x for x in new_intervals if abs(x) > Step]
        self.notes      += [x % Octave for x in new_notes]

    def ExtendStats(self, new_notes):
        #print("EXTENDING with", new_notes)
        #print("ME", self.length, self.melody)
        exMS = MelodyStats()
        exMS.length     = self.length
        exMS.melody     = self.melody[:]     
        exMS.intervals  = self.intervals[:]  
        exMS.directions = self.directions[:] 
        exMS.leaps      = self.leaps[:]      
        exMS.notes      = self.notes[:]
        exMS.add_notes(new_notes)
        #print("NEW", exMS.length, exMS.melody)
        return exMS

    def __str__(self):
        print_str = ""
        print_str += ("\nLegnth"     + str(self.length     ))
        print_str += ("\nMelody"     + str(self.melody     ))
        print_str += ("\nIntervals"  + str(self.intervals  ))
        print_str += ("\nDirections" + str(self.directions ))
        print_str += ("\nLeaps"      + str(self.leaps      ))
        print_str += ("\nNotes"      + str(self.notes      ))
        return print_str
        
        
    
### First, checks that can be done only on the last one or two entries
def check_no_leaps_larger_than_octave(lps): # last leap
    # let's disallow octaves as well, because they rarely sound good
    if not any([abs(x) >= P8 for x in lps]):
        return True
    else:
        if verbose: print('fail: no_leaps_larger_than_octave in ' + str(m))

def check_no_dissonant_leaps(lps):         # last leap
    consonant = [M3, P4, P5, m6, P8]
    if not any([abs(x) not in consonant for x in lps]):
        return True
    else:
        if verbose: print('fail: no_dissonant_leaps in ' + str(m))
        
def check_larger_leaps_followed_by_change_of_direction(m, invs, dirs): # 2 interval & 2 directions
    for i in range(len(m) - 2):
        if abs(invs[i]) > 4 and dirs[i] == dirs[i + 1]:
            if verbose: print ('fail: larger_leaps_followed_by_change_of_direction in ' + str(m))
            return False
    return True

def check_leading_note_goes_to_tonic(m): # last two notes
    for i in range(len(m) - 1):
        if m[i] %12 == 11 and m[i+1]%12 != 0:
            if verbose: print ('fail: leading_note_goes_to_tonic in ' + str(m))
            return False
    return True

def check_no_same_two_intervals_in_a_row(m, invs): # last 2 intervals 
    for i in range(len(m) - 2):
        if invs[i] > Step and invs[i] == - invs[i + 1]:
            if verbose: print ('fail: no_same_two_intervals_in_a_row in ' + str(m))
            return False
    return True
    
def check_no_noodling(m, invs): # Last 3 intervals
    for i in range(len(m) - 3):
        if invs[i] == - invs[i + 1] and invs[i + 1] == - invs[i + 2]:
            if verbose: print ('fail: no_noodling in ' + str(m))
            return False
    return True

def check_no_long_runs(m,dirs):  # Last 4 notes
    if len(dirs)<4: return True
    d = dirs[-4:]
    
    if dirs.count(d[0]) == len(d):
        if verbose: print ('fail: no_long_runs in ' + str(dirs) + ' : ' + str(m))
        return False
    return True
    # runs = get_runs_from_melody(m)
    # for run in runs:
    #     if len(run) > 4:
    #         if verbose: print ('fail: no_long_runs in ' + str(m) + ' : ' + str(runs))
    #         return False
    # return True

# Only requires the last 4 notes to see if it is a run and is not resolved.
def check_no_unresolved_melodic_tension(m, dirs):
    consonant_movements = [m3, M3, P4, P5, m6, P8]

    m_five = m[-4:]
    d = dirs[-3:]
    if len(d)<4:
        return True

    #If it's not a run, nothing to fear:
    if not (d[0] == d[1]):
        return True

    # If it is a run, it's lenght is 3 or 4 (less is not a run more is not allowed)
    if d[0] == d[2]:
        #Then the run was just 4 long        
        movement = abs(m_five[0] - m_five[4])
    else:
        #Then the run was just 3 long
        movement = abs(m_five[0] - m_five[3])
    
    if movement not in consonant_movements:
        if verbose: print ('fail: no_unresolved_melodic_tension in ' + str(m) + ' : ' + str(dirs))
        return False
    return True
     
    
        
        
def check_melody_last_bit(melodyStats, type, verbose, just_last = True):
    if just_last:
        """Optimization to reduce recomputation. We reduce the lists to the
        minimum needed to calculate the last added note
        """
        m     = melodyStats.melody[-2:]
        invs  = melodyStats.intervals[-3:]  
        dirs = melodyStats.directions[-4:] 
        lps      = melodyStats.leaps[-1:]      
    else:
        melody     = melodyStats.melody     
        invs  = melodyStats.intervals  
        dirs = melodyStats.directions 
        lps      = melodyStats.leaps

    def half00() : return check_leading_note_goes_to_tonic(m) and check_no_same_two_intervals_in_a_row(m, invs)
    def half01() : return check_larger_leaps_followed_by_change_of_direction(m, invs, dirs) and check_no_dissonant_leaps(lps)
    def half10() : return check_no_leaps_larger_than_octave(lps)
    def half11() : return check_no_noodling(m, invs) and check_no_long_runs(m,dirs) and check_no_unresolved_melodic_tension(m, dirs)

    return half00() and half01() and half10() and half11()

## Those that need the entire history
def check_melody_all(melodyStats, type, verbose):
    m          = melodyStats.melody     
    invs  = melodyStats.intervals  
    dirs = melodyStats.directions 
    lps      = melodyStats.leaps
    notes      = melodyStats.notes
        
    # There is also between_two_and_four_leaps(), which is global
    def at_most_four_leaps():
        if len(lps) <= 4:
            return True
        else:
            if verbose: print('fail: between_two_and_four_leaps in ' + str(m))
            
    def no_sequences():
        triples = [m[i:i+3] for i in range(len(m)-2)]
        normalized_triples = [(0, t[1]-t[0], t[2]-t[0]) for t in triples]

        if len(normalized_triples) == len(set(normalized_triples)): # no duplicates
            return True
        else:
            if verbose: print ('fail: no_sequences in ' + str(m) + ' : ' + str(normalized_triples))
            return False
        
    def no_repetition():
        if type == 'cantus': # no repetition allowed in cantus firmus
            if not 0 in invs:
                return True
            else:
                if verbose: print('fail: no_repetition in cantus firmus: ' + str(m))
        elif type == 'lead': # one repetition allowed in first species
            if invs.count(0) <= 1:
                return True
            else:
                if verbose: print('fail: no_repetition in first species: ' + str(m))
        else:
             if verbose: print('fail: unrecognized type', type)
        return False
    
    def no_note_repeated_too_often():
        for note in notes:
            if notes.count(note) > 3:
                if verbose: print('fail: no_note_repeated_too_often in ' + str(m))
                return False
        return True

    def no_more_than_two_consecutive_leaps_in_same_direction():
        for i in range(len(m) - 2):
            if abs(invs[i]) > Step and abs(invs[i + 1]) > Step and dirs[i] == dirs[i + 1]:
                if verbose: print ('fail: no_more_than_two_consecutive_leaps_in_same_direction in ' + str(m))
                return False
        return True
    
    return at_most_four_leaps() and no_sequences() and no_repetition() and no_note_repeated_too_often() and no_more_than_two_consecutive_leaps_in_same_direction()


def check_melody_idependent(notes, melodyStats, type, verbose, just_last = True):
    extended_melody = melodyStats.ExtendStats(notes)
    return (check_melody_last_bit(extended_melody, type, verbose, just_last)
            and check_melody_all(extended_melody, type, verbose))

        
def check_harmony_independent(lead, cantus, verbose = True):
    vertical_intervals = [abs(cantus[i] - lead[i]) for i in range(len(cantus))]
    v_i = vertical_intervals

    def no_dissonant_intervals():
        consonant = [Unison, m3, M3, P5, m6, M6]
        if not any([(x % Octave) not in consonant for x in vertical_intervals]):
            return True
        else:
             if verbose: print ('fail: no_dissonant_intervals error: ' + str(vertical_intervals))
             return False

    def no_intervals_larger_than_12th():
        return not any([x > (P8 + P5) for x in vertical_intervals])

    def no_parallel_fifths_or_octaves():
        for i in range(len(cantus) - 1):
            if (v_i[i] == P5 and v_i[i+1] == P5) or (v_i[i] == P8 and v_i[i+1] == P8):
                if verbose: print ('fail: no_parallel_fifths_or_octaves in vertical intervals: ' + str(vertical_intervals))
                return False
        return True

    def no_parallel_chains():
        if len(v_i) < 4:
            return True
        for i in range(len(cantus) - 3):
            if v_i[i] == v_i[i+1] and v_i[i+1] == v_i[i+2] and v_i[i+2] == v_i[i+3]:
                if verbose: print ('fail: no_parallel_chains in vertical intervals: ' + str(vertical_intervals))
                return False
        return True
    
    return no_parallel_fifths_or_octaves() and no_parallel_chains() and no_dissonant_intervals() and no_intervals_larger_than_12th()

#TODO: When a global fails, we should backtrack more then one
#step. Otherwise we are stuck on a bunch of wrong branches, until they
#all inevitably fail.
def check_globals_independent(m, verbose=False):
    intervals = [m[i+1] - m[i] for i in range(len(m) - 1)]
    #dirs = [sign(intervals[i]) for i in range(len(intervals))]
    lps = [x for x in intervals if abs(x) > Step]
    #notes = [x % Octave for x in m]
    
    # There is also at_most_four_leaps, which is local
    def between_two_and_four_leaps():
        if len(lps) in [2, 3, 4]:
            return True
        else:
            if verbose: print('Glob fail: between_two_and_four_leaps in ' + str(m), "\n Leaps", lps, "\n Intervals", intervals)

    def has_climax(): #Global
        # climax can't be on tonic or leading tone
        climax = max(m)
        position = [i for i, j in enumerate(m) if j == climax][0]
        if climax%Octave not in [Tonic, LeadingTone] and m.count(climax) == 1 and (position + 1) != (len(m) - 1):
            return True
        else:
            if verbose: print('Glob fail: has_climax in ' + str(m))

    def changes_direction_several_times(): #Global
        #TODO: this shouldn't be intervals, it should be direction changes! no?
        directional_changes = [intervals[i+1] - intervals[i] for i in range(len(m) - 2)]
        if len([x for x in directional_changes if x < 0]) >= 2:
            return True
        else:
            if verbose: print('Glob fail: changes_direction_several_times in ' + str(m))

    def final_note_approached_by_step(): #Global
        if abs(m[-1] - m[-2]) <= Step:
            return True
        else:
            if verbose: print ('Glob fail: final_note_approached_by_step in ' + str(m))

    return between_two_and_four_leaps() and has_climax() and changes_direction_several_times() and final_note_approached_by_step()
