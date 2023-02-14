import module.module as M
import module.everyman_module as EM
import module.opening_practice as OP
import module.stockfish as SF

prep_practice = OP.OpeningPracticeModule
average_player = EM.EverymanModule
stockfish_module = SF.StockfishModule
train_your_dragon = lambda : M.ModuleProduct3(prep_practice,
                                                average_player,
                                                stockfish_module)
pvp = M.PvP

available_modules = {"Train Your Dragon": train_your_dragon,
                     "PvP": pvp,
                     "Stockfish": stockfish_module,
                     "Prep practice": prep_practice,
                     "Average player": average_player}
available_modules_names = available_modules.keys()
default_module = "Train Your Dragon"
