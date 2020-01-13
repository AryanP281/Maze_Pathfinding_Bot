#****************************************Imports********************************
import sys
import time
import Gui
import Bot

#****************************************Functions********************************
def solve_maze(grid_dimensions, obstacle_coords, start_pos, end_pos) :
    """Solves the given maze"""

    start = time.time()
    path = Bot.solve_maze(grid_dimensions, end_pos, start_pos, obstacle_coords)
    print("Elapsed time = {}".format(time.time() - start))

    Gui.display_path(path)

#****************************************Script Commands********************************
Gui.initialize(solve_maze) #Initializing the program
