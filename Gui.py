#****************************************Imports********************************
import tkinter as tk
from tkinter import messagebox as msgbox

#****************************************Global Variables********************************
gui_elements = {} #All the gui elements in the main window
grid_dimensions = [] #The dimensions of the maze grid
obstacle_coords = [] #The coordinates obstructions in the maze
maze_solver_func = None #The function to be called to solve the maze i.e when confirm is pressed
end_pos = None #The coordinates of the "end" tile
start_pos = None #The coordinates of the "start" tile

#****************************************Main Functions********************************
def initialize(solve_maze_func) :
    """Initializes the app"""

    global maze_solver_func
    maze_solver_func = solve_maze_func

    #Getting the grid details
    get_grid_size()

def get_grid_size() :
    """Gets the size of the grid"""

    #Initializing the window
    grid_input_window = tk.Tk(None, None, " Grid Data") #A window for the user to input grid details
    #Setting the window size and position
    window_size = (400, 400) #The size of the window
    screen_size = (grid_input_window.winfo_screenwidth(), grid_input_window.winfo_screenheight()) #The size of the screen
    window_position = ((screen_size[0] / 2) - (window_size[0] / 2), (screen_size[1] / 2) - (window_size[1] / 2)) #The position of the window
    grid_input_window.geometry(f"{window_size[0]}x{window_size[1]}+{int(window_position[0])}+{int(window_position[1])}") #Setting the size and position
    grid_input_window.resizable(False, False) #Disabling window resizing

    #[Initializing the frame
    frame_size = (window_size[0] / 2, window_size[0] / 2)
    frame_rel_pos = (0.5 - ((frame_size[0] / window_size[0]) / 2), 0.5 - ((frame_size[1] / window_size[1]) / 2))
    frame = tk.Frame(grid_input_window, width=frame_size[0], height=frame_size[1])
    frame.place(relx=frame_rel_pos[0], rely=frame_rel_pos[1])
    frame.update_idletasks()

    #Initializing the labels
    row_label = tk.Label(frame, text="Rows:", font=('', 15))
    column_label = tk.Label(frame, text="Columns:", font=('', 15))
    row_label_rel_pos = (0, 0.25)
    column_label_rel_pos = (0, 0.4)
    row_label.place(relx=row_label_rel_pos[0], rely=row_label_rel_pos[1])
    column_label.place(relx=column_label_rel_pos[0], rely=column_label_rel_pos[1])
    row_label.update_idletasks()
    column_label.update_idletasks()

    #Initializing the entries
    row_entry = tk.Entry(frame)
    column_entry = tk.Entry(frame)
    row_entry_rel_pos = (row_label_rel_pos[0] + (row_label.winfo_width() / frame.winfo_width()) + 0.05, 
    row_label_rel_pos[1] + 0.01)
    column_entry_rel_pos = (column_label_rel_pos[0] + (column_label.winfo_width() / frame.winfo_width()) + 0.05, 
    column_label_rel_pos[1] + 0.01)
    row_entry.place(relx=row_entry_rel_pos[0], rely=row_entry_rel_pos[1])
    column_entry.place(relx=column_entry_rel_pos[0], rely=column_entry_rel_pos[1])

    #Initializing the confirm button
    button_command = initialize_grid_dimension_saver_func(row_entry, column_entry, grid_input_window)
    confim_button = tk.Button(frame, font=('', 15), text="Confirm", command=button_command)
    confim_button_rel_pos = (0.25, column_label_rel_pos[1] + 0.25)
    confim_button.place(relx=confim_button_rel_pos[0], rely=confim_button_rel_pos[1])

    grid_input_window.mainloop() #Starting the GUI loop

def initalize_gui() :
    """Initializes the gui elements"""

    #Initializing the main window of the program
    initialize_main_window()
    
    #Initializing the grid
    initialize_grid_gui()

    #Initializes the remaining gui elements
    initialize_remaining_gui()

def initialize_main_window() : 
    """Initializes the main window of the program"""

    main_window = tk.Tk() #Creating a instance of the window

    #Setting the window size and position
    window_size = (800, 800) #The size of the main window
    screen_size = (main_window.winfo_screenwidth(), main_window.winfo_screenheight()) #The size of the screen
    window_position = ((screen_size[0] / 2) - (window_size[0] / 2), (screen_size[1] / 2) - (window_size[1] / 2)) #The position of the window
    main_window.geometry(f"{window_size[0]}x{window_size[1]}+{int(window_position[0])}+{int(window_position[1])}") #Setting the size and position
    main_window.resizable(False, False) #Preventing resizing of window
    main_window.title("Path Finder Bot") #Setting the title of the window
    main_window.update_idletasks() #Updating the window geometry
    
    #Adding the window to the dictionary of GUI elements in the scene
    global gui_elements
    gui_elements["windows"] = {"main_window" : main_window} #Adding the window to the dictionary of GUI elements in the scene

def initialize_grid_gui() :
    """Displays the grid on the main window"""

    #Loading a global variable
    global gui_elements

    #Initailizing a frame for the grid buttons
    #The size of the frame
    frame_size = (int(0.5 * gui_elements["windows"]["main_window"].winfo_width()), 
    int(0.5 * gui_elements["windows"]["main_window"].winfo_height())) 
    #The position of the frame relative to the main window
    frame_rel_pos = (0.5 - (frame_size[0] / (2 * gui_elements["windows"]["main_window"].winfo_width())), 
    0.5 - (frame_size[1] / (2 * gui_elements["windows"]["main_window"].winfo_height())))
    frame = tk.Frame(gui_elements["windows"]["main_window"], width=frame_size[0], height=frame_size[1], bg="navy") #Creating the frame
    frame.grid_propagate(False) #Preventing resizing of frame according to the widgets it contains
    frame.place(relx=frame_rel_pos[0], rely=frame_rel_pos[1]) #Placing the frame
    frame.update_idletasks() #Updating frame geometry

    #Adding the frame to the dictionary of GUI elements in the scene
    gui_elements["frames"] = {"grid_frame": frame}

    #Creating the grid
    create_grid(frame)

def initialize_remaining_gui() :
    """Initializes the GUI used for specifying the start and end of the maze and the confirm button"""

    #Initializing the frame
    frame_size = (gui_elements["windows"]["main_window"].winfo_width(), 
    (gui_elements["windows"]["main_window"].winfo_height() - gui_elements["frames"]["grid_frame"].winfo_height()) / 4) #Calculating the size of the frame
    frame_rel_pos = (0.0, 0.0) #Calculating the position of the frame relative to the main window
    frame = tk.Frame(gui_elements["windows"]["main_window"], width=frame_size[0], height=frame_size[1]) #Creating the frame
    frame.grid_propagate(False) #Preventing resisizing of frame
    frame.place(relx=frame_rel_pos[0], rely=frame_rel_pos[1]) #Placing the frame
    #Configuring the rows and columns in the frame's grid
    for row in range(0,2) :
        frame.grid_rowconfigure(row, weight=1)
    for col in range(0,8) :
        frame.grid_columnconfigure(col, weight=1)
    #Adding the frame to the dictionary of gui elements on the scene
    gui_elements["frames"]["start_end_spec_frame"] = frame

    #Initializing the labels
    start_label = tk.Label(frame, text="Start Postion:-", font=("", 15))
    start_label.grid(row=0,column=0,sticky="nwse")
    start_row_label = tk.Label(frame, text="Row=")
    start_row_label.grid(row=0,column=2, sticky="nwse")
    start_column_label = tk.Label(frame, text="Column=")
    start_column_label.grid(row=0, column=6, sticky="nswe")
    end_label = tk.Label(frame, text="End Position:-", font=("", 15))
    end_label.grid(row=1,column=0, sticky="nwse")
    end_row_label = tk.Label(frame, text="Row=")
    end_row_label.grid(row=1,column=2, sticky="nwse")
    end_column_label = tk.Label(frame, text="Column=")
    end_column_label.grid(row=1,column=6, sticky="nwse")
    #Adding the labels to the dictionary of gui elements on the scene
    gui_elements["labels"] = {
        "start_pos_label": start_label,
        "end_pos_label": end_label,
        "start_row_label": start_row_label,
        "start_column_label": start_column_label,
        "end_row_label": end_row_label,
        "end_column_label": end_column_label
        }

    #Initializing the row and column entries
    start_row_entry = tk.Entry(frame)
    start_row_entry.grid(row=0, column=3, sticky="nsew")
    start_col_entry = tk.Entry(frame)
    start_col_entry.grid(row=0, column=7, sticky="nsew")
    end_row_entry = tk.Entry(frame)
    end_row_entry.grid(row=1, column=3, sticky="nsew")
    end_col_entry = tk.Entry(frame)
    end_col_entry.grid(row=1, column=7, sticky="nsew")
    #Adding the entries to the dictionary of gui elements on the scene
    gui_elements["entries"] = {
        "start_row_entry": start_row_entry,
        "start_col_entry": start_col_entry,
        "end_row_entry": end_row_entry,
        "end_col_entry": end_col_entry
    }

    #Initializing the confirm button
    btn = tk.Button(gui_elements["windows"]["main_window"], text="Confirm", font=("", 15), command=confirm_maze)
    btn.place(relx=0.46, rely=0.8)
    #Adding the button to the dictionary of gui elements on the scene
    gui_elements["buttons"] = {"confirm_button": btn}

def display_path(path) :
    """Displays the given path on a grid"""
    
    #Creating a new window for the displaying the path
    result_window = tk.Tk()
    #The string describing the window's geometry
    geometry_string = "{}x{}+{}+{}".format(gui_elements["frames"]["grid_frame"].winfo_width(), 
    gui_elements["frames"]["grid_frame"].winfo_height(), 
    gui_elements["frames"]["grid_frame"].winfo_x(), gui_elements["frames"]["grid_frame"].winfo_y())
    #Setting the window size and position
    result_window.geometry(geometry_string)
    result_window.title("Solved maze") #Changing the title of the window
    result_window.resizable(False, False) #Preventing resisizing of the window
    result_window.grid_propagate(False)

    #Creating labels representing the maze grid
    for row in range(0, grid_dimensions[0]) :
        result_window.grid_rowconfigure(row, weight=1) #Configuring the row
        for col in range(0, grid_dimensions[1]) :
            result_window.grid_columnconfigure(col, weight=1) #Configuring the column
            bg = "" #The background of the tile label
            text = "" #The text to display in the tile label
            if((row, col) in path and (row,col) != start_pos and (row,col) != end_pos) :
                bg = "green" #Making tiles in the path green
            elif((row, col) in obstacle_coords) :
                bg = "red" #Making obstacle tiles red
            elif((row, col) == end_pos) :
                bg = "maroon" #Making the end tile maroon
                text = "End"
            elif((row, col) == start_pos) :
                bg = "yellow" #Making the start tile yellow
                text = "Start"
            else :
                bg = "white" #Making normal tiles white
            tile = tk.Label(result_window, bg=bg, relief="solid",text=text) #Creating the tile label
            tile.grid(row=row,column=col,sticky="nsew") #Placing the tile
    
    result_window.mainloop()
    gui_elements["windows"]["main_window"].destroy()

#****************************************Helper Functions********************************

def initialize_grid_dimension_saver_func(row_entry, column_entry, grid_data_window) :
    """Acts as a wrapper for get_grid_dimensions(), so that it can be given as a command to the confirm button"""

    def get_grid_dimensions() :
        """Parses and saves the grid dimensions and begins initialization of the main window"""

        try :
            global grid_dimensions #Reference to the global variable
            grid_dimensions.extend([int(row_entry.get()), int(column_entry.get())]) #Parsing and saving the inputs from the GUI Entries
            grid_data_window.destroy() #Closes the grid input window
            initalize_gui() #Begins gui initialization
        except ValueError :
            msgbox.showerror("Error", "Invalid grid dimensions")
            grid_data_window.destroy()
            get_grid_size()

    return get_grid_dimensions

def create_grid(frame) :
    """Creates the gui buttons representing the grid"""

    maze_grid = [] #The grid of buttons

    #Looping through the rows
    for row in range(0, grid_dimensions[0]) :
        maze_grid.append([]) #Adding a new row in the grid
        frame.grid_rowconfigure(row, weight=1) #Configuring the row column
        #Looping through the columns
        for column in range(0, grid_dimensions[1]) :
            frame.grid_columnconfigure(column, weight=1) #Configuring the frame column

            cmd = grid_editor_wrapper(row,column) #The button click event
            btn = tk.Button(frame, command=cmd, bg="white") #Creating a button
            btn.grid(row=row, column=column, sticky="nsew") #Placing the button in the frame's grid
            maze_grid[row].append(btn) #Adding the button to the maze grid

    global gui_elements
    gui_elements["maze_grid"] = maze_grid #Adding the grid of buttons to the gui elements

def grid_editor_wrapper(row, col) :
    """Acts as a wrapper for the function which is called when a grid button is pressed"""

    def edit_grid() :
        """Edits the maze grid"""

        #Loading a global variable
        global obstacle_coords

        #Checking if the tile is an obstacle or a free tile
        if(((row, col) in obstacle_coords) == False) :
            #Changing background colour of button
            gui_elements["maze_grid"][row][col].config(bg="red")

            #Updating the list of obstructions
            obstacle_coords.append((row, col))

        else :
            #Changing background colour of button
            gui_elements["maze_grid"][row][col].config(bg="white")

            #Updating the list of obstructions
            obstacle_coords.remove((row, col))


    return edit_grid

def confirm_maze() :
    """Called when the confirm button is pressed. Confirms the maze to be solved"""
    try:
        #Loading global variables
        global start_pos
        global end_pos
        
        #Getting the maze start and end coordinates
        start_pos = (int(gui_elements["entries"]["start_row_entry"].get()), int(gui_elements["entries"]["start_col_entry"].get()))
        end_pos = (int(gui_elements["entries"]["end_row_entry"].get()), int(gui_elements["entries"]["end_col_entry"].get()))

        #Checking if entered coordinates are valid
        if(start_pos[0] >= grid_dimensions[0] or end_pos[0] >= grid_dimensions[0] or start_pos[1] >= grid_dimensions[1] or end_pos[1] >= grid_dimensions[1]) :
            raise Exception("Invalid coordinates")

        #Calling the maze solver function
        global maze_solver_func
        maze_solver_func(grid_dimensions, obstacle_coords, start_pos, end_pos)

    except ValueError:
        print("Invalid coordinates")

