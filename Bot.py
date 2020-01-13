"""Solves the maze using A* algorithm"""

#****************************************Imports********************************

#****************************************Classes********************************
class Node(object) :
    def __init__(self, coords, goal_coords, current_path_length) :
        """Sets the attributes of the node"""

        self.coords = coords #The coordinates of the node

        #Calculating the g(n) value of node
        self.calculate_gn_value(current_path_length)

        #Calculating the h(n) value of node
        self.calculate_hn_value(goal_coords)

        #Calculating f(n) value of node
        self.calculate_fn_value()

    def calculate_gn_value(self, current_path_length) :
        """Calculates the g(n) value if the node is traversed"""

        self.gn_value = (current_path_length) #The g(n) value is the distance of the path if the node is traversed

    def calculate_hn_value(self, goal_coords) :
        """Calculates the h(n) value of the node"""

        #The h(n) value is the Manhattan distance of node from goal node
        self.hn_value = abs(self.coords[0] - goal_coords[0]) + abs(self.coords[1] - goal_coords[1]) 

    def calculate_fn_value(self) :
        """Calculates the f(n) value of the node"""

        self.fn_value = self.gn_value + self.hn_value #f(n) = g(n) + h(n)

    def __eq__(self, other) :
        """Overloading == operator"""

        if(self.coords == other.coords) :
            return True
        return False

#****************************************Global Variables********************************
grid_dims = None #The dimensions of the maze grid
goal_pos = None #The coordinates of the goal node
obstacle_coords = [] #The coordinates of the obstacles on the grid
open_list = [] #A list of the next possible node to move to
closed_list = [] #A list of the already traversed nodes

#****************************************Functions********************************
def solve_maze(grid_dimensions, goal_position, start_position, obstacle_coordinates) :
    """Solves the maze"""
    
    reset_bot() #Resetting the bot before solving a new maze

    #Setting the parameters before starting
    global grid_dims
    grid_dims = grid_dimensions
    global goal_pos
    goal_pos = goal_position
    global obstacle_coords
    obstacle_coords = obstacle_coordinates

    #Adding the start position to the closed_list
    closed_list.append(Node(start_position, goal_position, 0))

    #Traversing the maze
    paths = [] #A list of the paths traversed
    paths.append([closed_list[0]]) #Adding a new path
    path = traverse_maze(paths, paths[0]) #Getting the path

    return get_path_coordinates(path)

def reset_bot() :
    """Resets the bot to solve a new maze"""

    open_list.clear()
    closed_list.clear()

def traverse_maze(paths, current_path) :
    """Traverses the maze"""

    #Getting the traversible nodes connected to the current node
    connected_nodes = get_connected_nodes(current_path[-1], current_path.__len__())

    #Checking if the goal can be reached
    if(Node(goal_pos, goal_pos, current_path.__len__()) in connected_nodes) :
        current_path.append(Node(goal_pos, goal_pos, current_path.__len__() + 1))
        closed_list.append(current_path[-1])
        return current_path

    #Adding the connected nodes to the open_list
    open_list.extend(connected_nodes)

    #Selecting the next node to travel to
    next_node = get_next_node()

    #Removing the next node from open list and adding to closed list
    open_list.remove(next_node)
    closed_list.append(next_node)

    #Checking if the next node belongs to the current path or to a different path
    if(not next_node in connected_nodes) :
        new_path = manage_paths(next_node, paths) #Creating a new path-branch
        paths.append(new_path) #Adding the new path to the list of paths
        return traverse_maze(paths, new_path) #Traversing the new path
    else :
        next_node.gn_value = current_path.__len__() #Updating the node's g(n) value
        current_path.append(next_node) #Adding the node to the current path
        return traverse_maze(paths, current_path)

def get_connected_nodes(node, current_path_len) :
    """Gets the traversible nodes connected to the given node"""

    connected_nodes = [] #A list of the connected nodes
    closed_list_coords = get_path_coordinates(closed_list)

    #Checking if the node belongs to the 1st row
    if(node.coords[0] != 0) :
        connected_node = Node((node.coords[0] - 1, node.coords[1]), goal_pos, current_path_len)
        #Checking if the node has already been traversed or is it is an obstacle
        if(not connected_node.coords in closed_list_coords and not connected_node.coords in obstacle_coords) :
            connected_nodes.append(connected_node)

    #Checking if the node belongs to the last row
    if(node.coords[0] != grid_dims[0] - 1) :
        connected_node = Node((node.coords[0] + 1, node.coords[1]), goal_pos, current_path_len)
        #Checking if the node has already been traversed or is it is an obstacle
        if(not connected_node.coords in closed_list_coords and not connected_node.coords in obstacle_coords) :
            connected_nodes.append(connected_node)

    #Checking if the node belongs to the 1st column
    if(node.coords[1] != 0) :
        connected_node = Node((node.coords[0], node.coords[1] - 1), goal_pos, current_path_len)
        #Checking if the node has already been traversed or is it is an obstacle
        if(not connected_node.coords in closed_list_coords and not connected_node.coords in obstacle_coords) :
            connected_nodes.append(connected_node)

    #Checking if the node belongs to the 1st column
    if(node.coords[1] != grid_dims[1] - 1) :
        connected_node = Node((node.coords[0], node.coords[1] + 1), goal_pos, current_path_len)
        #Checking if the node has already been traversed or is it is an obstacle
        if(not connected_node.coords in closed_list_coords and not connected_node.coords in obstacle_coords) :
            connected_nodes.append(connected_node)

    return connected_nodes

def get_node_coordinates(nodes) :
    """Returns a list containing the coordinates of the given nodes"""

    coords = [] #The list of coordinates

    for node in nodes :
        coords.append(node.coords)

    return coords

def get_next_node() :
    """From the open_list, selects the next node to travel to"""

    #Checking if any traversible nodes are left
    if(open_list.__len__() == 0) :
        raise Exception("No traversible nodes left")

    next_nodes = get_node_with_lowest_fn(open_list) #Getting the list of nodes having min. f(n) value

    #In case of multiple nodes, returning the node with lowest h(n) value
    if(next_nodes.__len__() > 1) :
        return get_node_with_lowest_hn(next_nodes)

    return next_nodes[0]

def get_node_with_lowest_fn(nodes) :
    """Returns the node with the lowest f(n) value"""

    next_nodes = [nodes[0]] #The nodes having the lowest f(n) value
    min_fn = next_nodes[0].fn_value

    for a in range(1, nodes.__len__()) :
        if(nodes[a].fn_value < min_fn) :
            next_nodes.clear()
            next_nodes.append(nodes[a])
        elif(nodes[a].fn_value == min_fn) :
            next_nodes.append(nodes[a])

    return next_nodes

def get_node_with_lowest_hn(nodes) :
    """From open_list, returns the node having lowest h(n) value"""

    node = nodes[0]
    min_hn = node.hn_value

    for a in range(1, nodes.__len__()) :
        if(nodes[a].hn_value < min_hn) :
            node = nodes[a]
            min_hn = node.hn_value

    return node

def manage_paths(node, paths) :
    """Creates a new path branch"""

    #Getting the nodes neighbouring the given node
    neighbours = get_neighbouring_nodes(node) 

    #Creating a new path branch
    new_path = [] #The new path
    path_found = False #Indicates whether the path to which the node belongs has been found

    #Looping through the neighbours
    for neighbour in neighbours :
        for path in paths :
            #Checking whether the path contains the neighbour
            if(neighbour in path) :
                index = path.index(neighbour)
                #Checking if the branch belongs to the current path
                if(path[index].gn_value == neighbour.gn_value) :
                    new_path = path[:index + 1] + [node] #Creating a new path branch
                    new_path[-1].gn_value = new_path.__len__() - 1 #Updating the node's g(n) value
                    path_found = True
                    break
        if(path_found) :
            break
    
    if(not path_found) :
        raise Exception("No branch junction found")

    #Setting the new path as the current path
    return new_path

def get_neighbouring_nodes(node) :
    """Returns the nodes neighbouring the given node"""

    connected_nodes = [] #A list of the connected nodes

    #Checking if the node belongs to the 1st row
    if(node.coords[0] != 0) :
        connected_node = Node((node.coords[0] - 1, node.coords[1]), goal_pos, node.gn_value - 1)
        #Checking if the node is an obstacle
        if(not connected_node.coords in obstacle_coords) :
            connected_nodes.append(connected_node)

    #Checking if the node belongs to the last row
    if(node.coords[0] != grid_dims[0] - 1) :
        connected_node = Node((node.coords[0] + 1, node.coords[1]), goal_pos, node.gn_value - 1)
        #Checking if the node is an obstacle
        if(not connected_node.coords in obstacle_coords) :
            connected_nodes.append(connected_node)

    #Checking if the node belongs to the 1st column
    if(node.coords[1] != 0) :
        connected_node = Node((node.coords[0], node.coords[1] - 1), goal_pos, node.gn_value - 1)
        #Checking if the node is an obstacle
        if(not connected_node.coords in obstacle_coords) :
            connected_nodes.append(connected_node)

    #Checking if the node belongs to the 1st column
    if(node.coords[1] != grid_dims[1] - 1) :
        connected_node = Node((node.coords[0], node.coords[1] + 1), goal_pos, node.gn_value - 1)
        #Checking if the node is an obstacle
        if(not connected_node.coords in obstacle_coords) :
            connected_nodes.append(connected_node)

    return connected_nodes

def get_path_coordinates(path) :
    """Returns the coordinates of the nodes in the path"""

    coords = []

    for node in path :
        coords.append(node.coords)

    return coords
