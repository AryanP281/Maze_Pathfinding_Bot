#****************************************Imports********************************

#****************************************Classes********************************
class Bot(object) :
    def __init__(self, learning_rate = 0.4) :
        """Class constructor"""

        #Initializing the class attributes
        self.maze = [] #A 2d representation of the maze
        self.learning_rate = learning_rate #Setting the learning rate of the bot
        self.end_pos = None #The target position
        self.obstacle_coords = [] #The positions of the obstacles

    def train(self,grid_dims, end_pos, obstacle_coords) :
        """Trains the bot on the given """

        #Setting the target position
        self.end_pos = end_pos
        #Setting the positions of the obstacles
        self.obstacle_coords = obstacle_coords

        #Traversing through the maze and getting the paths to the endpoint
        paths = self.traverse_maze(grid_dims)

       #Adjusting the values in the maze
        self.analyse_paths(paths)

    def traverse_maze(self, grid_dims) :
        """Traverses the maze"""

        #Initializing the maze structure and gets all possible start positions
        start_positions = self.initialize_maze(grid_dims)

        #Checking if the has a starting point
        if(start_positions.__len__() != 0) :
            #Getting all the possible paths to the end
            paths = [] #The paths to the end
            self.traverse_path(paths, [start_positions[0]], self.get_connected_tiles) #Traversing the maze from the 1st possible start position

            #Traversing from the remaining possible start positions
            for pos in start_positions :
                self.traverse_path(paths, [pos], self.get_connected_tiles)

            return paths

        else :
            raise Exception("Invalid maze")
    
    def initialize_maze(self, grid_dims) :
        """Initializes the maze structure and returns all possible start positions"""

        start_pos = [] #A list of all the possible start positions

        #Looping through the rows
        for row in range(0, grid_dims[0]) :
            self.maze.append([]) #Adding a row to the maze structure
            #Looping through the columns
            for col in range(0, grid_dims[1]) :
                #Checking if the tile is the end position
                if((row, col) == self.end_pos) :
                    self.maze[row].append(1.0)
                #Checking if tile has an obstacle
                elif((row, col) in self.obstacle_coords) :
                    self.maze[row].append(-1.0)
                #For normal tiles
                else :
                    self.maze[row].append(0.0)
                    start_pos.append((row, col)) #Adding the tile to the list of possible starting positions
        
        return start_pos   

    def traverse_path(self, paths, current_path, get_connected_tiles) :
        """Traverses a given path"""

       #Checking if its the end tile
        if(current_path[len(current_path) - 1] == self.end_pos) :
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
                self.traverse_path(paths, path, get_connected_tiles) #Traversing the new path

            self.traverse_path(paths, current_path, get_connected_tiles) #Further traversing the current path
    
    def get_connected_tiles(self, current_path) :
        """Returns all the tiles connected to the current tile"""

        next_moves = [] #A list of the connected tiles
        current_tile = current_path[len(current_path) - 1] #The coordinates of the current position

        #Checking if tile belongs to the 1st row
        if(current_tile[0] != 0) :
            #Adding the tile above the current tile to the list
            if(not (current_tile[0] - 1, current_tile[1]) in current_path and not (current_tile[0] - 1, current_tile[1]) in self.obstacle_coords) :
                next_moves.append((current_tile[0] - 1, current_tile[1]))
        #Checking if tile belongs to the last row
        if(current_tile[0] != len(self.maze) - 1) :
            #Adding the tile below the current tile to the list
            if(not (current_tile[0] + 1, current_tile[1]) in current_path and not (current_tile[0] + 1, current_tile[1]) in self.obstacle_coords) :
                next_moves.append((current_tile[0] + 1, current_tile[1]))
        #Checking if the tile belongs to the 1st column
        if(current_tile[1] != 0) :
            #Adding the tile to the left of current tile to the list
            if(not (current_tile[0], current_tile[1] - 1) in current_path and not (current_tile[0], current_tile[1] - 1) in self.obstacle_coords) :
                next_moves.append((current_tile[0], current_tile[1] - 1))
        #Checking if the tile belongs to the last column
        if(current_tile[1] != len(self.maze[0]) - 1) :
            #Adding the tile to the right to the list
            if(not (current_tile[0], current_tile[1] + 1) in current_path and not (current_tile[0], current_tile[1] + 1) in self.obstacle_coords) :
                next_moves.append((current_tile[0], current_tile[1] + 1))

        return next_moves

    def analyse_paths(self, paths) :
        """Calculates and sets the tile values"""

        #Looping through the paths
        for path in paths :
            #Looping through the steps in the path
            for tile_index in range(len(path) - 2, 0, -1) :
                current_tile = path[tile_index] #The current tile
                next_tile = path[tile_index + 1] #The next step in the path
                #Calculating the increment in the value of the tile
                change = self.learning_rate * (self.maze[next_tile[0]][next_tile[1]] - self.maze[current_tile[0]][current_tile[1]])
                self.maze[path[tile_index][0]][path[tile_index][1]] += change #Changing the value of the tile

    def solve_maze(self, start_pos) :
        """Finds the shortest path from starting position to the end"""

        #Finding all the paths to the target
        paths = [] #The paths to the target
        current_path = [start_pos] #The path being currently traversed
        self.traverse_path(paths, current_path, self.get_connected_tiles_by_value)

        #Checking if a path was found
        if (len(paths) == 0) :
            raise Exception("No path found")

        #Finding and returning the shortest path
        return self.get_shortest_path(paths)

    def get_shortest_path(self, paths) :
        """Returns the shortest path out of the list of """

        shortest = [paths[0].__len__(), paths[0]] #The length of the shortest path
        for path in paths :
            if(path.__len__() < shortest[0]) :
                shortest[0] = path.__len__()
                shortest[1] = path

        return shortest[1]

    def get_connected_tiles_by_value(self, current_path) :
        """Returns the connected tiles having the highest values"""

        next_moves = [] #A list of the connected tiles
        current_tile = current_path[len(current_path) - 1] #The coordinates of the current position
        max_val = 0.0 #The max value of any of the neighbouring tiles

        #Checking if tile belongs to the 1st row
        if(current_tile[0] != 0) :
            #Checking if the tile above the current tile has a greater value than current max
            if(self.maze[current_tile[0] - 1][current_tile[1]] > max_val) :
                #Checking if the tile has already been travesed
                if(not (current_tile[0] - 1, current_tile[1]) in current_path) :
                    next_moves.clear() #Removing the earlier moves
                    next_moves.append((current_tile[0] - 1, current_tile[1])) #Adding the move to the list
                    max_val = self.maze[current_tile[0] - 1][current_tile[1]] #Updating the max value
             #Checking if the tile above the current tile has a value equal to the current max
            elif (self.maze[current_tile[0] - 1][current_tile[1]] == max_val and self.maze[current_tile[0] - 1][current_tile[1]] != self.maze[current_tile[0]][current_tile[1]]) :
                #Checking if the tile has already been travesed or is an obstacle
                if(not (current_tile[0] - 1, current_tile[1]) in current_path) :
                    next_moves.append((current_tile[0] - 1, current_tile[1])) #Adding the move to the list
        
        #Checking if tile belongs to the last row
        if(current_tile[0] != len(self.maze) - 1) :
            #Checking if the tile below the current tile has a greater value than current max
            if(self.maze[current_tile[0] + 1][current_tile[1]] > max_val ) :
                #Checking if the tile has already been travesed or is an obstacle
                if(not (current_tile[0] + 1, current_tile[1]) in current_path) :
                    next_moves.clear() #Removing the earlier moves
                    next_moves.append((current_tile[0] + 1, current_tile[1])) #Adding the move to the list
                    max_val = self.maze[current_tile[0] + 1][current_tile[1]] #Updating the max value
             #Checking if the tile below the current tile has a value equal to the current max
            elif (self.maze[current_tile[0] + 1][current_tile[1]] == max_val and self.maze[current_tile[0] + 1][current_tile[1]] != self.maze[current_tile[0]][current_tile[1]]) :
                #Checking if the tile has already been travesed or is an obstacle
                if(not (current_tile[0] + 1, current_tile[1]) in current_path) :
                    next_moves.append((current_tile[0] + 1, current_tile[1])) #Adding the move to the list

        #Checking if tile belongs to the 1st column
        if(current_tile[1] != 0) :
            #Checking if the tile to the left of current tile has a greater value than current max
            if(self.maze[current_tile[0]][current_tile[1] - 1] > max_val) :
                #Checking if the tile has already been travesed or is an obstacle
                if(not (current_tile[0], current_tile[1] - 1) in current_path) :
                    next_moves.clear() #Removing the earlier moves
                    next_moves.append((current_tile[0], current_tile[1] - 1)) #Adding the move to the list
                    max_val = self.maze[current_tile[0]][current_tile[1] - 1] #Updating the max value
             #Checking if the tile to the left of current tile has a value equal to the current max
            elif (self.maze[current_tile[0]][current_tile[1] - 1] == max_val and self.maze[current_tile[0]][current_tile[1] - 1] != self.maze[current_tile[0]][current_tile[1]]) :
                 #Checking if the tile has already been travesed or is an obstacle
                if(not (current_tile[0], current_tile[1] - 1) in current_path) :
                    next_moves.append((current_tile[0] - 1, current_tile[1])) #Adding the move to the list

        #Checking if tile belongs to the last column
        if(current_tile[1] != len(self.maze[0]) - 1) :
            #Checking if the tile to the right of current tile has a greater value than current max
            if(self.maze[current_tile[0]][current_tile[1] + 1] > max_val) :
                 #Checking if the tile has already been travesed or is an obstacle
                if(not (current_tile[0], current_tile[1] + 1) in current_path) :
                    next_moves.clear() #Removing the earlier moves
                    next_moves.append((current_tile[0], current_tile[1] + 1)) #Adding the move to the list
                    max_val = self.maze[current_tile[0]][current_tile[1] + 1] #Updating the max value
             #Checking if the tile to the left of current tile has a value equal to the current max
            elif (self.maze[current_tile[0]][current_tile[1] + 1] == max_val and self.maze[current_tile[0]][current_tile[1] + 1] != self.maze[current_tile[0]][current_tile[1]]) :
                #Checking if the tile has already been travesed or is an obstacle
                if(not (current_tile[0], current_tile[1] + 1) in current_path) :
                    next_moves.append((current_tile[0], current_tile[1] + 1)) #Adding the move to the list

        return next_moves


