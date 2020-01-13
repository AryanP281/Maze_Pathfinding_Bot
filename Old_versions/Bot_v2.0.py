#****************************************Imports********************************

#****************************************Global Variables********************************
grid_dims = [] #The dimensions of the maze grid
end_pos = None #The position to be reached
obstacle_coords = [] #The coordinates of the obstacles in the maze

#****************************************Functions********************************
def solve_maze(grid_dimensions, start_pos, end_position, obstacle_coordinates) :
    """Solves the given maze"""

    #Assigining values to global variables
    global grid_dims
    grid_dims = grid_dimensions
    global end_pos
    end_pos = end_position
    global obstacle_coords
    obstacle_coords = obstacle_coordinates

    #Finding all the paths to the end
    paths = [] #The paths to the end
    current_path = [start_pos] #The path currently being traversed
    traverse_path(paths, current_path) #Traversing the maze

    #Checking if a path was found
    if (paths.__len__() == 0) :
        raise Exception("No path found")

    #Finding and returning the shortest path
    return get_shortest_path(paths)

def traverse_path(paths, current_path) :
    """Traverses the given path"""

    #Checking if its the end tile
    if(current_path[len(current_path) - 1] == end_pos) :
        paths.append(current_path) #Adding the path to the list of paths to the destination
        return #Ending recursion
       
    #Getting the next tiles that can be moved to
    next_pos = get_connected_tiles(current_path)

    #Checking if there are any possible moves left
    if(len(next_pos) != 0) :
        current_path.append(next_pos[0]) #Updating the current path
        #Creating new paths for all remaining options
        for pos in range(1, len(next_pos)) :
            path =  current_path[:len(current_path) - 1] + [next_pos[pos]] #Creating a new path
            traverse_path(paths, path) #Traversing the new path

        traverse_path(paths, current_path) #Further traversing the current path

def get_connected_tiles(current_path) :
    """Returns all the tiles connected to the current tile"""

    next_moves = [] #A list of the connected tiles
    current_tile = current_path[len(current_path) - 1] #The coordinates of the current position

    #Checking if tile belongs to the 1st row
    if(current_tile[0] != 0) :
        #Adding the tile above the current tile to the list
        if(not (current_tile[0] - 1, current_tile[1]) in current_path and not (current_tile[0] - 1, current_tile[1]) in obstacle_coords) :
            next_moves.append((current_tile[0] - 1, current_tile[1]))
    #Checking if tile belongs to the last row
    if(current_tile[0] != grid_dims[0] - 1) :
        #Adding the tile below the current tile to the list
        if(not (current_tile[0] + 1, current_tile[1]) in current_path and not (current_tile[0] + 1, current_tile[1]) in obstacle_coords) :
            next_moves.append((current_tile[0] + 1, current_tile[1]))
    #Checking if the tile belongs to the 1st column
    if(current_tile[1] != 0) :
        #Adding the tile to the left of current tile to the list
        if(not (current_tile[0], current_tile[1] - 1) in current_path and not (current_tile[0], current_tile[1] - 1) in obstacle_coords) :
            next_moves.append((current_tile[0], current_tile[1] - 1))
    #Checking if the tile belongs to the last column
    if(current_tile[1] != grid_dims[1] - 1) :
        #Adding the tile to the right to the list
        if(not (current_tile[0], current_tile[1] + 1) in current_path and not (current_tile[0], current_tile[1] + 1) in obstacle_coords) :
            next_moves.append((current_tile[0], current_tile[1] + 1))

    return next_moves

def get_shortest_path(paths) :
    """Returns the shortest path out of the list of """

    shortest = [paths[0].__len__(), paths[0]] #The length of the shortest path
    for path in paths :
        if(path.__len__() < shortest[0]) :
            shortest[0] = path.__len__()
            shortest[1] = path

    return shortest[1]

