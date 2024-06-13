# This is a python program written by Paul Gan, Robert Tsai, Cameron Guo, &
# Cyrus Kirkman. The goal of the program was to create a "stained-glass" type
# of canvas for participants to draw on.

# It was last updated June 5, 2024

"""
Noah's Art Program Version 2.0 (Stained Glass)
==================

Introduction
------------
The Noah's Art Program allows a wide range of species to create digital artwork
using a touchscreen. This project includes a control panel for selecting pigeon
subjects and a painting interface where the actual art creation happens. The
program operates in two modes: an operant box environment and a regular desktop
setup.

Program Overview
----------------
1. **ExperimenterControlPanel Class**:
    - Initializes a control panel for selecting pigeon subjects.
    - Allows users to select a pigeon name from a dropdown menu.
    - On selection and starting the program, it sets up directories for saving
      data.
    - Launches the main painting interface.

2. **Point Class**:
    - Represents a point in the painting application.
    - Stores coordinates and an index.

3. **Paint Class**:
    - Manages the painting interface where the artwork is created.
    - Initializes the drawing canvas, either in fullscreen mode
      (for operant box) or windowed mode (for desktop).
    - Handles user inputs for drawing on the canvas.
    - Saves the artwork to a specified directory.
    - Binds keys for various functions like toggling lines, toggling labels,
      and exiting the program.

4. **Graph Class**:
    - Represents a graph structure for managing points and their connections.
    - Stores vertex angles and regions, used for more complex operations
      related to the artwork.

5. **Main Function**:
    - Sets up the Tkinter root window for the painting interface.
    - Binds mouse and keyboard events to the Paint class methods.
    - Runs the Tkinter main loop to keep the application running.

Control Flow
------------
1. When the script is executed, an instance of `ExperimenterControlPanel`
   is created.
2. The control panel window appears, prompting the user to select a pigeon name.
3. Upon clicking the "Start program" button, the selected pigeon name is passed
   to the main painting interface.
4. The `Paint` class sets up the drawing canvas based on the environment
   (operant box or desktop).
5. Users can interact with the canvas to create artwork, using the left mouse
   button to draw and the right mouse button to cancel.
6. The artwork is saved when the user presses the `Escape` key to exit the
   program.

Mention global variables that others will change (specify #row)
                                                  
"""

# First we import the libraries relevant for this project
from tkinter import Tk, Canvas, BOTH
# Tkinter is used for creating graphical user interfaces.
# Here, Tk initializes the main window, Canvas is used for drawing graphics,
# and BOTH is used to specify that widgets should expand to fill any extra space.

from tkinter import messagebox
# Import messagebox from tkinter for displaying pop-up messages to the user,
# useful for alerts and confirmations.

import functools
# Import functools for higher-order functions that act on or return other functions.
# Often used for function decorators, partials, and other utility functions.

from time import perf_counter
# Import perf_counter from time module for high precision timing,
# useful for benchmarking code segments.

from datetime import datetime, date
# Import datetime and date to handle date and time data,
# useful for timestamps and scheduling within the application.

from random import randint
# Import randint from the random module to generate random integer values,
# possibly for random positioning or choices.

from os import path, getcwd, mkdir
# os module imports for file and directory management.
# 'path' for path manipulations, 'getcwd' to get the current working directory,
# and 'mkdir' to create new directories.

from csv import writer, QUOTE_MINIMAL
# Import writer and QUOTE_MINIMAL from the csv module for writing to CSV files
# with minimal quoting around each field, typically for data storage.

from PIL import Image
# Import Image from PIL (Python Imaging Library) to handle image file operations,
# which could be used for processing or displaying images.

from csv import reader
# Import reader from the csv module to read from CSV files,
# useful for loading previously saved data.

from math import atan2, pi
# Import atan2 and pi from the math module. atan2 computes the arc tangent of two variables,
# useful for angle calculations,
# and pi is the mathematical constant π, used in angle and circle calculations.

import os
from tkinter import *
from tkinter import Tk, Canvas, OptionMenu, StringVar, Label, Button
from os import path as os_path, getcwd, mkdir
from datetime import datetime, date
from csv import reader

# The first variable declared is whether the program is the operant box version
# for pigeons, or the test version for humans to view. The variable below is 
# a T/F boolean that will be referenced many times throughout the program 
# when the two options differ (for example, when the Hopper is accessed or
# for onscreen text, etc.). It is changed automatically based on whether
# the program is running in operant boxes (True) or not (False). It is
# automatically set to True if the user is "blaisdelllab" (e.g., running
# on a rapberry pi) or False if not. The output of os_path.expanduser('~')
# should be "/home/blaisdelllab" on the RPis

# Updated to run on 1024x768p screens.

if path.expanduser('~').split("/")[2] =="blaisdelllab":
    operant_box_version = True
    print("*** Running operant box version *** \n")
else:
    operant_box_version = False
    print("*** Running test version (no hardware) *** \n")
    
# Global variables 
TIME = 0 # Gives a metric for relevative efficiency

# User-defined variables for directory paths
OPERANT_BOX_DATA_DIR = str(path.expanduser('~')) + "/Desktop/Data/P033_data/P033c_StainedGlass_Data"
DESKTOP_DATA_DIR = getcwd() + "/P033c_StainedGlass_Data"


if operant_box_version:
    data_folder_directory = OPERANT_BOX_DATA_DIR
else:
    data_folder_directory  = DESKTOP_DATA_DIR

# Create macro folder if it does not exist
try:
    if not path.isdir(data_folder_directory):
        mkdir(path.join(data_folder_directory))
        print("\n ** NEW DATA FOLDER FOR %s CREATED **")
except FileExistsError:
    print("Data folder for %s exists.")
    
## Define functions:
    
# Timer (for debugging).
# Remember to remove the @timer decorator calls if deleting this function.
def timer(func):
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        tic = perf_counter()
        value = func(*args, **kwargs)
        toc = perf_counter()
        elapsed_time = toc - tic
        if TIME:
            print(f"{func.__name__}: {elapsed_time:0.4f} seconds")
        return value
    return wrapper_timer

# Ensure operant_box_version is defined (set according to your initial check)
operant_box_version = path.expanduser('~').split("/")[2] == "blaisdelllab"

class ExperimenterControlPanel(object):
    def __init__(self):
        self.doc_directory = str(os_path.expanduser('~'))+"/Documents/"
        if operant_box_version:
            self.data_folder = "P003e_data" # The folder within Documents where subject data is kept
            self.data_folder_directory = str(os_path.expanduser('~'))+"/Desktop/Data/" + self.data_folder
        else: # If not, just save in the current directory the program is being run in 
            self.data_folder_directory = getcwd() + "/data"
            try:
                if not os_path.isdir(self.data_folder_directory):
                    mkdir(self.data_folder_directory)
                    print(f"\n ** NEW DATA FOLDER CREATED AT: {self.data_folder_directory}**")
            except FileExistsError:
                print(f"DATA FOLDER EXISTS AT: {self.data_folder_directory}")
        
        self.control_window = Tk()
        self.control_window.geometry("300x100")  # Set the size of the control panel window
        self.control_window.title("Noah's Art Control Panel")
        self.pigeon_name_list = ["Mario", "Thoth", "Odin", "Itzamna", "Vonnegut", "Hawthorne", "Durrell"]
        self.pigeon_name_list.sort() # This alphabetizes the list
        self.pigeon_name_list.insert(0, "TEST")
        
        Label(self.control_window, text="Pigeon Name:").pack()
        self.subject_ID_variable = StringVar(self.control_window)
        self.subject_ID_variable.set("Select")
        self.subject_ID_menu = OptionMenu(self.control_window,
                                          self.subject_ID_variable,
                                          *self.pigeon_name_list,
                                          command=self.set_pigeon_ID).pack()
        
        # Start button
        self.start_button = Button(self.control_window,
                                   text = 'Start program',
                                   bg = "green2",
                                   command = self.build_chamber_screen).pack()
        
        # This makes sure that the control panel remains on screen until exited
        self.control_window.mainloop() # This loops around the CP object
        
    def set_pigeon_ID(self, pigeon_name):
        # This function checks to see if a pigeon's data folder currently 
        # exists in the respective "data" folder within the Documents
        # folder and, if not, creates one.
        try:
            if not os_path.isdir(self.data_folder_directory + "/" + pigeon_name):
                mkdir(os_path.join(self.data_folder_directory, pigeon_name))
                print("\n ** NEW DATA FOLDER FOR %s CREATED **" % pigeon_name.upper())
        except FileExistsError:
            print(f"DATA FOLDER FOR {pigeon_name.upper()} EXISTS")
                
    def build_chamber_screen(self):
        if self.subject_ID_variable.get() in self.pigeon_name_list:
            print("Operant Box Screen Built") 
            # Call the main Paint program here
            self.control_window.destroy()
            main(self.subject_ID_variable.get())
        else:
            print("\n ERROR: Input Correct Pigeon ID Before Starting Session")
            
class Point:
    def __init__(self, coord, ind): 
        # Initialize the Point class with coordinates and an index
        self.ind = ind     # Store the index of the point
        self.coord = coord # Store the coordinates of the point

class Paint:
    def __init__(self, root, artist_name):
    # Initialize the Paint class with a Tkinter root window and the artist's name.
        self.root = root
        if operant_box_version:
            # Set up for operant box version with predefined screen size and fullscreen.
            self.width, self.height = 1024, 768 # Set default dimensions for the canvas.
            
            # Set the geometry of the root window to fullscreen at these dimensions.
            self.root.geometry(f"{self.width}x{self.height}+{self.width}+0")
            self.root.attributes('-fullscreen',
                                 True)
            self.canvas = Canvas(root,
                                 bg="black")
            self.canvas.pack(fill = BOTH,
                                   expand = True)
            
            # Canvas save directory
            self.save_directory = str(path.expanduser('~'))+"/Desktop/Data/Pigeon_Art"

        else:
            # Set up for non-operant box version with fixed dimensions but not fullscreen.
            self.width, self.height = 1024, 768
            self.canvas = Canvas(root, width=self.width, height=self.height)
            self.canvas.pack()
            # Canvas save directory
            self.save_directory = getcwd() + "/saved_art/"
            try:
                # Attempt to create the directory if it doesn't exist.
                if not path.isdir(self.save_directory):
                    mkdir(path.join(self.save_directory))
            except FileExistsError:
                pass
            
        # Set up the directory to save data files, specific to each artist.
        try:
            if not path.isdir(data_folder_directory + artist_name):
                # Attempt to create a new data directory for the artist if it doesn't exist.
                mkdir(path.join(data_folder_directory, artist_name))
                print("\n ** NEW DATA FOLDER FOR %s CREATED **" % artist_name.upper())
        except FileExistsError:
            pass
            
        # Bind escape key
        root.bind("<Escape>", self.exit_program) # bind exit program to the "esc" key

        # variables needed for drawing
        self.x, self.y = None, None
        self.draw = False
        self.guideLine = None

        # store all demo label ids
        self.demoLabels = []

        # toggle variables
        self.demo = 0
        self.showLines = 1
        
        # Below, we store all necessary data
        self.currLineIndex = 0 # increment after every line drawn
        self.currPointIndex = 0 # increment after every point of intersection is found

        # Stores all lines and the lines they intersect with by their index
        # {line0 : [(line1, line2), (line3, line4)... ], ...}
        self.lines = {}

        # Store all line ids in a list. When we need to remove lines, this is useful.
        self.lineIds = []
        
        # An adjacency list to store all vertices and edges of our directed graph
        self.graph = {}

        # Stores all points of intersection
        # {line0 : [P1, P2, ... ]} where P1, P2, etc. are Point objects defined in the Point class
        self.intersects = {}

        # Maps line intersect coords to pos coords
        # {(lineIndex0, lineIndex1) : (x, y)}
        self.lineToPosCoords = {}

        # Maps point index to position coordinates
        self.pointToPosCoords = {}

        # Maps point position coordinates to indices
        self.posCoordsToPoints = {}

        # Maps point index (0-n) to their line indices (0-m)
        self.pointToLineIndices = {}

        # Stores all polygons and their ids
        # {[p1,p2,...pn] : id, ...}
        self.polygons = {}

        # Create data objects
        self.start_time = datetime.now() # Set start time
        
        # Stores the name of the painter
        self.subject = artist_name
        
        # Data is written every time a peck happens
        self.session_data_frame = [] #This where trial-by-trial data is stored
        data_headers = [
            "SessionTime", "IRI", "X1","Y1","PrevX","PrevY", "SizeOfLine", 
             "Event", "NPolygons","NDots", "NLines",  "NIslands", "NColors", 
             "BackgroundColor","StartTime", "Experiment", "P033_Phase",
             "PrevReinforcersEarned", "BoxNumber",  "Subject",  "Date"
            ]
        self.session_data_frame.append(data_headers) # First row of matrix is the column headers
        
        
        self.previous_response = datetime.now() # Will update with every peck
        
        # Stores the date of the painting
        self.date = date.today().strftime("%y-%m-%d")
        
        # Stores previous x-coordinate of point
        self.PrevX = "NA"
        self.PrevY = "NA"
        self.background_color = "NA" # Starts NA, gets changed at beginning of trial
        self.dot_counter = 0 # Counts the number of pecks
        self.num_islands = "NA"
        self.polygon_type = "NA"
        # This subject assigning process is limited to birds that are currently running
        if self.subject in ["Durrell","Peach","Luigi","Odin", "Hawthorne",
                       "Waluigi", "Wario", "Wenchang"]:
            self.experiment = "P034b"
        elif self.subject in ["Athena", "Bon Jovi", "Cousteau", "Darwin",
                         "Shy Guy", "Bowser", "Yoshi"]:
            self.experiment = "P035"
        elif self.subject in ["Zappa", "Joplin", "Ozzy", "Sting",
                         "Jagger", "Iggy", "Evaristo", "Kurt"]:
            self.experiment = "P037"
        else:
            self.experiment = "NA"
            
        if operant_box_version:
            box_num_csv_path = "/home/blaisdelllab/Desktop/Box_Info/Box_number.txt"
            with open(box_num_csv_path, 'r') as file:
                f = reader(file)
                # Assuming there is only one row and one column in the CSV file...
                for row in f:
                    # Convert the value to the appropriate data type (e.g., int)
                    self.box_num = int(row[0])
        else:
            self.box_num = "NA"
            
        self.prev_reinforcers_earned = "NA"
        self.P033_phase = "P033c-LinesWhileDrawing"

        # make the entire canvas a polygon
        offset = 4
        self.drawLine([(0-offset, 0-offset),
                       (self.width+offset, 0-offset)]) # upper-left to upper-right
        self.drawLine([(self.width+offset, 0-offset),
                       (self.width+offset, self.height+offset)]) # upper-right to lower-right
        self.drawLine([(self.width+offset, self.height+offset),
                       (0-offset, self.height+offset)]) # lower-right to lower-left
        self.drawLine([(0-offset, self.height+offset),
                       (0-offset, 0-offset)]) # lower-left to upper-left
        
        # # Remove lines from drawing (can add back in with keybound command)
        # self.toggleLines("event")
        
    # generates a random color
    def generateColor(self):
        rand = lambda: randint(50, 200)
        color_choice = '#%02X%02X%02X' % (rand(), rand(), rand())
        if self.background_color == "NA":
            self.background_color = color_choice
        return color_choice
    

    # Return true if line segments AB and CD intersect.
    # This will be used in the findIntersects method
    def hasIntersect(self, A, B, C, D):
        def ccw(A,B,C):
            return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])
        return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)

    # Every time a line segment is drawn, we will call this function on that line segment
    # For each line that the new line intersects, we will append the intersect coord (x, y) to 
    # the values (lists) of both lines in self.intersects
    # Return all intersects between line and all stored lines as a list of 2D points
    @timer
    def findIntersects(self, line):
        # helper function to find intersection between 2 lines
        def getIntersect(line1, line2):

            xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
            ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

            def det(a, b):
                return a[0] * b[1] - a[1] * b[0]

            div = det(xdiff, ydiff)
            if div == 0:
                return None

            d = (det(*line1), det(*line2))
            x = det(d, xdiff) / div
            y = det(d, ydiff) / div
            return (x, y)

        # loop through all stored lines, check intersect between line and each line l2 in list
        for lineNum, l2 in self.lines.items():
            if self.hasIntersect(line[0], line[1], l2[0], l2[1]) == False:
                continue
            p = getIntersect(line, l2)
            if p is not None: # if line and l2 intersecting
                self.lineToPosCoords[(lineNum, self.currLineIndex)] = p
                self.pointToPosCoords[self.currPointIndex] = p
                self.posCoordsToPoints[p] = self.currPointIndex

                # add indices of intersecting lines (values) associated with point (key) to the pointToLineIndices dict
                self.pointToLineIndices[self.currPointIndex] = [self.currLineIndex, lineNum]

                # update self.intersects dict
                self.intersects.setdefault(lineNum, []).append(Point(p, self.currPointIndex))
                self.intersects.setdefault(self.currLineIndex, []).append(Point(p, self.currPointIndex))
                
                # sort lists in self.intersects
                self.intersects[lineNum] = sorted(self.intersects[lineNum], key=lambda x : x.coord)
                self.intersects[self.currLineIndex] = sorted(self.intersects[self.currLineIndex], key=lambda x : x.coord)

                self.currPointIndex += 1

    # Function to update self.graph after new shapes are drawn onto canvas
    @timer
    def updateEdges(self):
        self.graph = {} # clear the graph

        # identify all points that are not involved in a cycle
        self.toExclude = set()
        for points in self.intersects.values():
            if len(points) == 1:
                self.toExclude.add(points[0].ind)

        for _list in self.intersects.values():
            if len(_list) < 2: continue
            for i in range(len(_list)-1):
                u, v = _list[i], _list[i+1]
                if (u.ind not in self.toExclude) and (v.ind not in self.toExclude):
                    self.graph.setdefault(u, []).append(v)

    # draws a red dot at specified point
    def drawDot(self, point):
        r = 6
        id = self.canvas.create_oval(point[0]-r//2, point[1]-r//2, point[0]+r//2, point[1]+r//2,
                                fill="#FF0000", outline="#FF0000")
        return id

    # function to find all new polygons since last shape drawn
    def findNewPolygons(self):
        def printPolygon(p, end='\n'):
            for point in p:
                print(self.posCoordsToPoints[point], end=' ')
            print(end=end)

        # if graph contains only 1 directed edge, there are no polygons
        if len(self.graph) <= 1:
            return None

        g = Graph(self.graph) # passing in directed graph
        regions = g.solve() # list of sublists containing point indices (0 - n)
        
        polygons = set()

        # for each polygon
        for r in regions:
            # convert point index to position coords
            polygon = [self.pointToPosCoords[p] for p in r] 

            # reorder polygon vertices while preserving edge relationships
            # we want the top-left-most vertex as the first item
            forwardList = polygon + polygon
            left = forwardList.index(min(polygon))
            if forwardList[left][0] > forwardList[left + 1][0]:
                forwardList.reverse() 
                left = forwardList.index(min(polygon))
            polygon = forwardList[left:left+len(polygon)]
            polygons.add(tuple(polygon))

        newPolygons = list(polygons - set(self.polygons.keys()))
        
        # if polygon is new
        for polygon in newPolygons:
            isNew = True
            # if polygon is already in stored polygons, don't add it again
            for curr in self.polygons.keys():
                currSet, polygonSet = set(curr), set(polygon)
                if currSet == polygonSet or len(currSet - polygonSet) == 0 or len(polygonSet - currSet) == 0: 
                    isNew = False
            
            # if new polygon, fill with random color and add its vertices and id to the polygons dict
            if isNew:
                color = self.generateColor()
                id = self.canvas.create_polygon(polygon, fill=color, outline=color, width=0.5)
                self.polygons[polygon] = id # add new polygon to list
                # 
        
        # print("polygons:")
        # for p in self.polygons:
        #     printPolygon(p, end=' | ')

    # redraw all lines
    def drawLines(self):
        # remove all current lines
        for id in self.lineIds:
            self.canvas.delete(id)
        
        self.lineIds = []
        
        # draw all lines
        for line in self.lines.values():
            id = self.canvas.create_line(line, width=0.5)
            self.lineIds.append(id)

    # function to extend line by a factor of d. 
    # this is useful for intersection detection
    def extendLine(self, line, d):
        p1, p2 = line[0], line[1]
        mag = ((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2) ** (1/2) # magnitude
        
        if mag != 0:
            # new coords
            x1 = p1[0] - d * (p2[0]-p1[0]) / mag
            y1 = p1[1] - d * (p2[1]-p1[1]) / mag
            x2 = p2[0] + d * (p2[0]-p1[0]) / mag
            y2 = p2[1] + d * (p2[1]-p1[1]) / mag
        else:
            # new coords
            x1 = p1[0] - d * (p2[0]-p1[0])
            y1 = p1[1] - d * (p2[1]-p1[1])
            x2 = p2[0] + d * (p2[0]-p1[0])
            y2 = p2[1] + d * (p2[1]-p1[1])
        
        return [(x1, y1), (x2, y2)]

    # draw line onto canvas, update data
    def drawLine(self, line):
        # increase line length slightly
        line = self.extendLine(line, 3)

        # sort line endpoints
        # if line is already in list, don't do anything
        line = sorted(line)
        if line in self.lines.values():
            print("line already drawn")
            return

        # find intersects between new line and all existing lines
        self.findIntersects(line)
        
        # add new line to lines dict
        self.lines[self.currLineIndex] = line

        # increment current line number
        self.currLineIndex += 1

        # update edges
        self.updateEdges()

        # find all polygons and fill them
        self.findNewPolygons()

        # draw all lines onto canvas
        if self.showLines: self.drawLines()

        if self.demo:
            self.drawDemoLabels()

    @timer
    def drawDemoLabels(self):
        for id in self.demoLabels:
            self.canvas.delete(id)
        self.demoLabels = []

        # draw edges
        for u in self.graph:
            for v in self.graph[u]:
                id = self.canvas.create_line((*u.coord, *v.coord), width=2, fill="blue", arrow='last')
                self.demoLabels.append(id)

        # draw point numbers
        for point, coord in self.pointToPosCoords.items():
            id = self.canvas.create_text(coord[0], coord[1] + 14, text=f"{point}")
            self.demoLabels.append(id)

        # draw points
        for point in self.lineToPosCoords.values():
            id = self.drawDot(point)
            self.demoLabels.append(id)

# Keybound commands:
    
    # callback for left click
    def onLeftButton(self, event):
        # Write a data event on every press
        if self.draw:
            self.drawLine([(self.x, self.y), (event.x, event.y)])
            if self.guideLine: self.canvas.delete(self.guideLine)
            self.draw = False
            self.x, self.y = None, None
        else:
            self.x, self.y = event.x, event.y
            self.draw = True
        # Write data for click
        self.write_data(event)

    # callback for right click
    def onRightButton(self, event):
        if self.draw:
            self.canvas.delete(self.guideLine)
            self.draw = False
            self.x, self.y = None, None

    # callback for mouse move
    def onMouseMove(self, event):
        # redraw guideline
        if self.guideLine: self.canvas.delete(self.guideLine)
        if self.x is not None and self.y is not None:
            self.guideLine = self.canvas.create_line((self.x, self.y, event.x, event.y), fill="red")

    def toggleLines(self, event):
        if not self.showLines:
            self.drawLines()
            self.showLines = 1
        else:
            # remove all current lines
            for id in self.lineIds:
                self.canvas.delete(id)
            self.showLines = 0

    def toggleDemo(self, event):
        if not self.demo:
            self.drawDemoLabels()
            self.demo = 1
        else:
            for id in self.demoLabels:
                self.canvas.delete(id)
            self.demoLabels = []
            self.demo = 0
        
    def write_data(self, event):
        # This function writes a new data line after EVERY peck. Data is
        # organized into a matrix (just a list/vector with two dimensions,
        # similar to a table). This matrix is appended to throughout the 
        # session, then written to a .csv once at the end of the session.
        if event != None: 
            x, y = event.x, event.y
            self.dot_counter += 1
            outcome = "peck"
        else: # There are certain data events that are not pecks.
            x, y = "NA", "NA"   
            outcome = "SessionEnds"
        
        # Line length calcultion
        if "NA" not in [self.PrevX, self.PrevY, x, y]:
            line_length = int(((x-self.PrevX)**2 + (y-self.PrevY)**2) ** 0.5) # Length of line rounded to nearest pixel
        else:
            line_length = "NA"
            
        self.session_data_frame.append([
            str(datetime.now() - self.start_time), # SessionTime as datetime object
            str(datetime.now() - self.previous_response), # IRI
            x, # X coordinate of a peck
            y, # Y coordinate of a peck
            self.PrevX, # Previous x coordinate
            self.PrevY, # Previous y coordinate
            line_length,
            outcome,
            len(self.polygons) - 1, # Number of polygons w/o background (?)
            self.dot_counter, # Number of points
            len(self.lineIds) - 4, # Number of lines
            self.num_islands, # EMPTY
            "NA", # "N colors",
            self.background_color,
            self.start_time,
            self.experiment,
            self.P033_phase,
            self.prev_reinforcers_earned,
            self.box_num,
            self.subject,
            date.today() # Today's date as "MM-DD-YYYY"
            ])
        
        # Update the "previous" response time
        if event != None:
            self.previous_response = datetime.now()
            self.PrevX = x
            self.PrevY = y
        
        data_headers = [
            "SessionTime", "IRI", "X1","Y1","PrevX","PrevY", "SizeOfLine", 
             "Event", "NPolygons","NDots", "NLines",  "NIslands", "NColors", 
             "BackgroundColor","StartTime", "Experiment", "P033_Phase",
             "PrevReinforcersEarned", "BoxNumber",  "Subject",  "Date"
            ]

        
    def write_comp_data(self):
        # The following function creates a .csv data document. It is called once
        # the session finishes (SessionEnded). If the first time the 
        # function is called, it will produce a new .csv out of the
        # session_data_matrix variable, named after the subject, date, and
        # training phase.
        self.write_data(None) # Writes end of session row to df
        myFile_loc = f"{data_folder_directory}/{self.subject}/P033c_{self.subject}_{self.start_time.strftime('%Y-%m-%d_%H.%M.%S')}_StainedGlassData3-LinesRemoved.csv" # location of written .csv
        
        # This loop writes the data in the matrix to the .csv              
        edit_myFile = open(myFile_loc, 'w', newline='')
        with edit_myFile as myFile:
            w = writer(myFile, quoting=QUOTE_MINIMAL)
            w.writerows(self.session_data_frame) # Write all event/trial data 
            print(f"\n- Data file written to {myFile_loc}")
            
    def exit_program(self, event):
        print("Escape key pressed")
        # Remove lines from drawing (can add back in with keybound command)
        self.toggleLines("event")
        print("- Lines removed from Canvas")
        self.write_comp_data()
        self.save_file()
        self.canvas.destroy()
        self.root.after(1, self.root.destroy())

    # This builds a popup save_file window and saves as a .eps file
    def save_file(self):
        list_of_options = ["Masterpiece", "Artwork", "Impressions", "Portrait",
                           "Future NFT", "Money-Maker", "Handiwork",
                           "Magnum Opus", "Craft", "Thesis Project",
                           "Life's Purpose"]
        rand_select_index = randint(0, len(list_of_options))
        rand_select = list_of_options[rand_select_index]
        if messagebox.askyesno("Save?", f"Save {self.subject}'s {rand_select}? \n (lines will be removed)"):
            now = datetime.now()
            file_name = f"{self.save_directory}/{self.subject}_{now.strftime('%m-%d-%Y_Time-%H-%M-%S')}_stained_glass_3"
            filepng = file_name + ".png"
    
            if not path.exists(filepng) or messagebox.askyesno("File already exists", "Overwrite?"):
                fileps = file_name + ".eps"
    
                self.canvas.postscript(file=fileps)
                #Image.open(fileps)
                #img.save(filepng, 'png')
                #os.remove(fileps)
    
                messagebox.showinfo("File Save", "File saved!")
            else:
                messagebox.showwarning("File Save", "File not saved!")

class Graph:
    def __init__(self, g):
        self.graph = g # undirected graph of Point objects {Point_0 : [point_1, Point_2...]}
        # sorted by vi as primary key and theta as secondary key
        self.vertexAngles = [] # [((vi, vj), theta), ...]
        self.wedges = []
        self.regions = []

    # find angle of line formed by 2 Point objects with respect to the horizontal
    # P1 will be the point of the angle
    def findAngle(self, P1, P2):
        y = P1.coord[1] - P2.coord[1]
        x = P2.coord[0] - P1.coord[0]
        if y == 0 and x == 0: return 0
        res = atan2(y, x) * 180 / pi
        return res if res >= 0 else (360+res)

    # helper function to get all ind values of Point objs in a wedge
    # returns a tuple (i1, i2, i3)
    def wedgeToIndices(self, wedge):
        return (wedge[0].ind, wedge[1].ind, wedge[2].ind)

    # binary search algorithm for finding next wedge from sorted wedge list
    # using v1 and v2 as primary and secondary search keys
    def searchWedge(self, v1, v2):
        l, r = 0, len(self.wedges)
        while l < r:
            m = (l+r) // 2
            # if middle element is what we are looking for, return the wedge
            if self.wedges[m][0].ind == v1 and self.wedges[m][1].ind == v2:
                return self.wedges[m]
            # else if middle element > v1, shrink right bound
            elif self.wedges[m][0].ind > v1: r = m
            # else if middle element < v1, shrink left bound
            elif self.wedges[m][0].ind < v1: l = m
            # else v1 matches but v2 doesn't, we adjust bound based on v2
            else:
                if self.wedges[m][1].ind > v2: r = m
                else: l = m
        
        # if we reach here -> element not found, return None
        return None

    def buildVertexAngles(self):
        for vi, edges in self.graph.items():
            for vj in edges:
                # Step 1: duplicate each undirected edge to form two directed edges
                e1, e2 = (vi, vj), (vj, vi)

                # Step 2: Complement each directed edge w/ angle theta of (vi, vj) 
                # w/ respect to horizontal line passing through vi. Add to list
                self.vertexAngles.extend([(e1, self.findAngle(e1[0], e1[1])), 
                                          (e2, self.findAngle(e2[0], e2[1]))])

        # Step 3: Sort list ascending by index and theta as primary and secondary keys
        self.vertexAngles = sorted(self.vertexAngles, 
                            key=lambda x: (x[0][0].ind, x[1]))

    def buildWedges(self):
        # Step 4: Combine consecutive entries in each group into a wedge
        firstInd = 0
        for i in range(1, len(self.vertexAngles)):
            if self.vertexAngles[i][0][0].ind == self.vertexAngles[i-1][0][0].ind:
                tup = (self.vertexAngles[i][0][1], self.vertexAngles[i][0][0], self.vertexAngles[i-1][0][1])
                self.wedges.append(tup)

            # last entry in group, add wedge
            if (i+1 >= len(self.vertexAngles)) or (self.vertexAngles[i+1][0][0].ind != self.vertexAngles[i][0][0].ind):
                tup = (self.vertexAngles[firstInd][0][1], self.vertexAngles[i][0][0], self.vertexAngles[i][0][1])
                # tup = (self.vertexAngles[i][0][1], self.vertexAngles[i][0][0], self.vertexAngles[firstInd][0][1])
                self.wedges.append(tup)
                firstInd = i + 1

    # this will return all faces of our planar graph
    def buildRegions(self):
        def findUnused():
            for k, v in self.used.items():
                if v == 0:
                    return k
            return None

        # Step 5: Sort wedge list using vi and vj as primary and secondary key
        self.wedges = sorted(self.wedges, key=lambda x: (x[0].ind, x[1].ind))

        # Step 6: Mark all wedges as unused
        self.used = {w:0 for w in self.wedges}

        # Step 7: Find unused wedge W0 = (v1, v2, v3)
        w0 = findUnused() # initial wedge: w0
        self.used[w0] = 1 # set w0 to used
        ind0 = self.wedgeToIndices(w0)
        nextFirst, nextSecond = ind0[1], ind0[2]
        wedgeList = [ind0]

        # Step 8: Search for next wedge wi = (v2, v3, vn)
        while self.used:
            wi = self.searchWedge(nextFirst, nextSecond) # O(logn) binary search
            self.used[wi] = 1 # set wi to used
            ind = self.wedgeToIndices(wi)
            nextFirst, nextSecond = ind[1], ind[2]
            wedgeList.append(self.wedgeToIndices(wi))

            # keep searching for next wedge until w(i+1) and w(1) are contiguous
            if (nextFirst != ind0[0]) and (nextSecond != ind0[1]): continue
            else: # contiguous region found
                region = [x[1] for x in wedgeList]
                # if region contains no repeating elements
                if len(region) > 2 and len(region) == len(set(region)): 

                    # _ = [print(x) for x in wedgeList]
                    # print()

                    self.regions.append(region) # store region
                
                wedgeList = [] # clear list

                # Back to Step 7: Find next unused wedge
                w0 = findUnused() # initial wedge: w0
                if not w0: break
                self.used[w0] = 1 # set w0 to used
                ind0 = self.wedgeToIndices(w0)
                nextFirst, nextSecond = ind0[1], ind0[2]
                wedgeList.append(ind0)
        
        # remove exterior face from our regions. (remove the longest list)
        # toRemove, longest = None, 0
        # for r in self.regions:
        #     if len(r) > longest:
        #         longest = len(r)
        #         toRemove = r
        # self.regions.remove(toRemove)

    # this function sequentially calls all functions in our pipeline
    def solve(self):
        self.buildVertexAngles()
        self.buildWedges()
        self.buildRegions()
        return self.regions

def main(artist_name):
    print("(l) toggle lines")
    print("(spacebar) toggle labels")
    print("left mouse button to draw")
    print("right mouse button to cancel draw")
    # Setup Canvas
    root = Tk()
    root.title("Paint Program with Polygon Detection")
    root.resizable(False, False)
    paint = Paint(root, artist_name) # Pass artist name to program
    # Bind out keys...
    root.bind("<ButtonPress-1>", paint.onLeftButton)
    root.bind("<ButtonPress-2>", paint.onRightButton)
    root.bind("<Motion>", paint.onMouseMove)
    root.bind("<space>", paint.toggleDemo)
    root.bind("l", paint.toggleLines)

    root.mainloop()

if __name__ == '__main__':
    cp = ExperimenterControlPanel()
