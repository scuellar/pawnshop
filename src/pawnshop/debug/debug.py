"""Simple tracing and debugging tools

Debugging is managed with global variables. That might be ugly but
it's good enough for this project.
"""

DEBUG_LEVEL = 0
EXEC_LOG = False
LOG = []

def trace(*args):
    """
    These are temporaty things you like to print.

    Shouldn't go in production
    """
    print(*args)

def debug(level, *args):
    if level <= 0:
        raise ("DEBUG LEVEL SET TOO LOW. Debug level must be higher than 0")
    if DEBUG_LEVEL >= level:
        print(*args)

def log(entry):
    """
    Adds one entry to the log
    """
    if EXEC_LOG:
        log = [entry
               ] ++ log
    
