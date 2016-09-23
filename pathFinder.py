 #!/usr/bin/env python
#Adam Sinck

#this is a list of import commands. If the user doesn't have Tkinter
#or other libraries installed, it will fail gracefully instead of
#crashing.
imports = [
    "from Tkinter import *",
    "import Tkinter as tk",
    "import tkMessageBox",
    "from ScrolledText import ScrolledText",
    "import tkFileDialog as tkf",
    "import string"
]
#failedPackages will keep a record of the names of the packages that
#failed to import, so that the program can go through the entire list
#of packages that it wants to import. This will allow the program to
#give the user a complete list of packages that they need to install,
#instead of only telling the user one at a time.
failedPackages = ''
for i in imports:
    try:
        exec(i)
    except ImportError as error:
        failedPackages += str(error) + '\n'
#if there were any errors in the imports, tell the user what packages
#didn't import, and exit.
if len(failedPackages) > 0:
    print "Some packages could not be imported:"
    print failedPackages
    exit()

#the maze text object
maze = None

#if the maze is displayed with ascii art or graphics
graphical = False

#the colors to use for the maze path
path = "#009900"
forward = "#000099"
back = "#990000"
success = "#550055"

#this holds the text representation of the maze. It can work with the
#text to decide legal moves, where the goal position is, etc.
class mazeText():

###########################################################################
##  Maze Text Initialization
###########################################################################

    #initialize the maze
    def __init__(self, fileName):
        self.maze = []
        text = open(fileName)
        for line in text:
            if (line[-1] == "\n"):
                self.maze.append(line[:-1])
            else:
                self.maze.append(line)
        text.close()

        self.height = 0
        self.width = 0
        self.moveTime = 0
        if (len(self.maze) > 0):
            self.height = len(self.maze)
            self.width = len(self.maze[0])
            self.moveTime = 1.0/((self.width + self.height)/2.0)
        
        self.start = (1, 1)
        self.goal = (self.width-1, self.height-1)

    #this sets a custom position for the start
    def setStartPosition(self, (x, y)):
        if (validPosition((x, y)) and self.maze[y][x] != "|"):
            self.start = (x, y)

    #this sets a custom position for the end
    def setGoalPosition(self, (x, y)):
        if (validPosition((x, y)) and self.maze[y][x] != "|"):
            self.goal = (x, y)
    
###########################################################################
##  Maze Text Game Solving
###########################################################################

    #this gets the valid moves from a position
    def getValidMoves(self, (x, y)):
        #the current position can't be on or outside boundary walls
        
        #note that height is downwards

        #because the left wall and top line are defined by
        #underscores, valid values begin at position (2, 2) and
        #run to (self.width-1, self.height-1)
        
        #note also that arrays and strings are 0 based, but self.width
        #and self.height are not
        if (not self.validPosition((x, y))):
            return []
        else:
            moves = []
            (current, N, S, E, W) = self.lookAround((x, y))
            #now that we've gotten the definitions all sewn up, do
            #position checks

            #South has to check if the current char is _ , or if S is |
            if (current != "_" and S != "|"):
                moves.append((x, y+1))
            #East has to check if E is |
            if (E != "|"):
                moves.append((x+1, y))
            #West has to check if W is |
            if (W != "|"):
                moves.append((x-1, y))
            #North has to check if N is _ or |
            if (N != "_" and N != "|"):
                moves.append((x, y-1))

            return moves

    #this gets all the characters in the area
    def lookAround(self, (x, y)):
        #North: y+1, x
        #South: y-1, x
        #East:  y, x+1
        #West:  y, x-1
        
        #return in order South, East, West, North, because I'm
        #assuming the path will start in the top left corner and
        #go to the bottom right corner
        current = self.maze[y][x]
        S = "|"
        if (y < self.height-1):
            S = self.maze[y+1][x]
        E = "|"
        if (x < self.width-1):
            E = self.maze[y][x+1]
        W = self.maze[y][x-1]
        N = self.maze[y-1][x]

        return (current, N, S, E, W)
    
###########################################################################
##  Maze Text Helper and info functions
###########################################################################

    #this returns if the given position is a valid one
    def validPosition(self, (x, y)):
        return (not (x >= self.width or y >= self.height or \
                     x <= 0 or y <= 0))

    #return if the position is the goal
    def isGoal(self, (x, y)):
        return (x == self.width-1 and y == self.height-1)

    #return the position of the start
    def getStartPosition(self):
        return self.start

    #return the position of the goal
    def getGoalPosition(self):
        return self.goal

    #return a text representation of the maze
    def getText(self):
        return "\n".join(self.maze)

###########################################################################
##  Maze Text Heuristics
###########################################################################

    #return the manhattan distance to the goal
    def manHeuristic(self, (x, y)):
        (goalX, goalY) = self.getGoalPosition()
        return abs(goalX - x) + abs(goalY - y)

    #return the euclidean heuristic the goal
    #I'm not sure this is useful given the manhattan heuristic, but
    #it's here because it could be and when it becomes useful it'll
    #already be here.
    def eucHeuristic(self, (x, y)):
        import math
        (goalX, goalY) = self.getGoalPosition()
        return math.sqrt(math.pow((goalX - x), 2) + math.pow((goalY - y), 2))


###########################################################################
##  Program helper functions
###########################################################################
        
#notDone will give a message saying that that feature is not complete
def notDone(var=None):
    tkMessageBox.showinfo("Not Ready", "This feature is not complete yet.")


###########################################################################
##  Program search functions
###########################################################################

#this does a dfs of the maze for the solution
def dfs():
    if (maze == None or maze.isGoal((1, 1))):
        return

    import time
    global path, forward, back
    
    resetMaze()

    #a list of positions visited already
    dejavu = []
    start = maze.getStartPosition()
    colorSpot(start, forward)
    
    queue = [start]

    node = prevNode = start
    while (len(queue) > 0):
        prevNode = node
        node = queue.pop()
        colorSpot(node, forward)
        if (mazeDisplay.tag_cget("(%d,%d)" %prevNode, "background") != back):
            colorSpot(prevNode, path)
        time.sleep(maze.moveTime)
        if (maze.isGoal(node)):
            return
        else:
            moves = maze.getValidMoves(node)[::-1]
            if (len(moves) == 1):
                time.sleep(maze.moveTime)
                colorSpot(node, back)
            for move in moves:
                if move not in dejavu:
                    dejavu.append(move)
                    queue.append(move)

#this is a breadth first search of the maze
def bfs():
    if (maze == None or maze.isGoal((1, 1))):
        return

    import time
    global path, forward, back
    
    resetMaze()

    class Node:
        def __init__(self, _node):
            self.path = []
            self.node = _node

    dejavu = []
    start = maze.getStartPosition()
    colorSpot(start, forward)

    startNode = Node(start)
    
    queue = [startNode]
    solution = []

    while (len(queue) > 0):
        node = queue.pop(0)
        colorSpot(node.node, forward)
        try: #color the parent, if there was one
            colorSpot(node.path[-2], path) #-2 because -1 is itself
        except:
            pass
        
        time.sleep(maze.moveTime)
        if (maze.isGoal(node.node)):
            solution = node.path
            queue = []
        else:
            #get the possible moves, but in reverse order because
            #we're using a queue and need to insert them in the
            #opposite order they're returned
            moves = maze.getValidMoves(node.node)[::-1]
            #If there is only one move, it's the parent and we're at a
            #dead end. If all the possible moves have already been
            #visited, then we're done in this branch.
            if ((len(moves) == 1) or \
                all((move in dejavu) for move in moves)):
                colorSpot(node.node, back)
            for move in moves:
                if move not in dejavu:
                    dejavu.append(move)
                    newNode = Node(move)
                    newNode.path = node.path + [move]
                    queue.append(newNode)


    # dejavu.append(start)
    # solution = solve([startNode])
    if (len(solution) > 0):
        colorSpot(start, success)
        for spot in solution:
            time.sleep(maze.moveTime/2.0)
            colorSpot(spot, success)

def aStar():
    if (maze == None):
        return

    import time, heapq

    resetMaze()
    
    class Node:
        def __init__(self, _node, _cost, _hcost):
            self.path = []
            self.node = _node
            self.cost = _cost
            self.hcost = _hcost
            
        #this is for sorting
        def __lt__(self, other):
            if (self.hcost < other.hcost):
                return True
            else:
                return self.cost < other.cost

        
    dejavu = []
    start = maze.getStartPosition()

    global path, forward, back

    colorSpot(start, forward)

    #if we're done, then we're done
    if (maze.isGoal(start)):
        return

    heuristic = maze.manHeuristic
    startNode = Node(start, 0, heuristic(start))

    def solve(queue):
        while (len(queue) > 0):
            item = heapq.heappop(queue)
            time.sleep(maze.moveTime)
            if maze.isGoal(item.node):
                colorSpot(item.node, forward)
                return item.path
            else:
                children = maze.getValidMoves(item.node)
                if ((len(children) == 1) or \
                    all((child in dejavu) for child in children)):
                    colorSpot(item.node, back)
                for child in children:
                    if (child not in dejavu):
                        if maze.isGoal(child):
                            return item.path + [child]

                        dejavu.append(child)
                        cost = item.cost + 1 #+1 because all steps cost 1
                        hcost = item.cost + heuristic(child)
                        node = Node(child, cost, hcost)
                        node.path = item.path + [child]
                        colorSpot(child, forward)
                        colorSpot(item.node, path)
                        heapq.heappush(queue, node)

    solution = solve([startNode])
    if (len(solution) > 0):
        colorSpot(start, success)
        for spot in solution:
            time.sleep(maze.moveTime/2.0)
            colorSpot(spot, success)

#This is like A* with path costs of 0 (that is to say, only the
#heuristic matters).
def closest():
    if (maze == None):
        return

    import time, heapq

    resetMaze()
    
    class Node:
        def __init__(self, _node, _hcost):
            self.path = []
            self.node = _node
            self.hcost = _hcost
            
        #this is for sorting
        def __lt__(self, other):
            return self.hcost < other.hcost

        
    dejavu = []
    start = maze.getStartPosition()

    global path, forward, back

    colorSpot(start, forward)

    #if we're done, then we're done
    if (maze.isGoal(start)):
        return

    heuristic = maze.manHeuristic
    startNode = Node(start, heuristic(start))

    def solve(queue):
        while (len(queue) > 0):
            item = heapq.heappop(queue)
            time.sleep(maze.moveTime)
            if maze.isGoal(item.node):
                colorSpot(item.node, forward)
                return item.path
            else:
                children = maze.getValidMoves(item.node)
                if ((len(children) == 1) or \
                    all((child in dejavu) for child in children)):
                    colorSpot(item.node, back)
                for child in children:
                    if (child not in dejavu):
                        if maze.isGoal(child):
                            return item.path + [child]

                        dejavu.append(child)
                        node = Node(child, heuristic(child))
                        node.path = item.path + [child]
                        colorSpot(child, forward)
                        colorSpot(item.node, path)
                        heapq.heappush(queue, node)

    solution = solve([startNode])
    if (len(solution) > 0):
        colorSpot(start, success)
        for spot in solution:
            time.sleep(maze.moveTime/2.0)
            colorSpot(spot, success)

###########################################################################
##  Program draw functions
###########################################################################

#this colors the spot at the given coordinates to be the given color
def colorSpot((x, y), color):
    global graphical
    if (graphical):
        # xposition = 20
        # yposition = 5
        # xoffset = 8#-(((maze.width-x)/(maze.width*1.0))*9)
        # yoffset = 16# - (((maze.height-y)/(maze.height*1.0))*16)
        # mazeCanvas.create_oval((x*xoffset)+xposition, (y*yoffset)+yposition, (x*xoffset)+10+xposition, (y*yoffset)+10+yposition, fill=color)
        # root.update_idletasks()
        pass
    else:
        #note: I adjusted the position of coloring because scrolled text
        #lines begin at 1 but characters at 0
        mazeDisplay.tag_delete("(%d,%d)" %(x, y))
        mazeDisplay.tag_add("(%d,%d)" %(x, y), "%d.%d" %(y+1, x), "%d.%d+1c" %(y+1, x))
        mazeDisplay.tag_config("(%d,%d)" %(x, y), background=color)
        root.update_idletasks()

#this resets the maze to the unsolved state
def resetMaze():
    global maze
    if maze == None:
        return
    global graphical
    if (graphical):
        pass
    else:
        mazeDisplay.config(state=NORMAL)
        mazeDisplay.delete("0.0", END)
        mazeDisplay.insert("0.0", maze.getText())
        mazeDisplay.config(state=DISABLED)
        global forward
        colorSpot((maze.getGoalPosition()), forward)

#this toggles if the ascii or the canvas representation of the maze is
#shown.
def toggleDisplay():
    global graphical
    if (graphical):
        mazeDisplay.pack(expand=YES, fill=BOTH)
        mazeCanvas.pack_forget()
        graphical = False
    else:
        mazeDisplay.pack_forget()
        mazeCanvas.pack(expand=YES, fill=BOTH)
        graphical = True
    resetMaze()

#this draws the initial maze
def drawMaze():
    global maze, graphical
    if (not graphical):
    
        #"draw" the ascii art in the text field
        mazeDisplay.config(state=NORMAL)
        mazeDisplay.delete("0.0", END)
        mazeDisplay.insert("0.0", maze.getText())
        mazeDisplay.config(state=DISABLED)
    else:
    
        #draw the maze in a canvas
        root.pack_propagate(False)
        global mazeCanvas
        mazeCanvas.pack_forget()
        mazeCanvas = Canvas(mazeFrame, bg="#FFF")
        mazeCanvas.config(width=maze.width, height=maze.height)
        mazeCanvas.pack(expand=YES, fill=BOTH)
        #root.pack_propagate(True)
        text = maze.getText()
        # x = 15
        # y = 10
        # charsize = 12
        #mazeCanvas.create_line(x, y, (x+1), (y+1))
        #mazeCanvas.create_text(x, y, text="")
        mazeCanvas.create_text((maze.width*5), (maze.height*8), text=text, font="Courier 10 bold")
        # mazeArray = text.split("\n")

        # for line in range(maze.height):
        #     y += charsize
        #     for character in range(maze.width):
        #         print mazeArray[line][character],
        #         if (mazeArray[line][character] == '_'): #draw a horizontal line
        #             # if (line < (maze.height-1) and mazeArray[line+1][character-1] == '|'):
        #             #     mazeCanvas.create_line(x-5, y, x, y, width=2)
        #             #mazeCanvas.create_text(x, y, text = "_", font="bold")
        #             mazeCanvas.create_line(x, y, x+charsize, y, width=2)
        #             # if (line < (maze.height-1) and mazeArray[line+1][character+1] == '|'):
        #             #     mazeCanvas.create_line(x+charsize, y, x+charsize+5, y, width=2)
        #         #draw a vertical line
        #         elif (mazeArray[line][character] == "|"):
        #             #mazeCanvas.create_text(x, y, text = "|", font="bold")
        #             # mazeCanvas.create_line(x, y+charsize, x+(charsize/2), y+charsize, width=2)
        #             mazeCanvas.create_line(x, y, x, y-charsize, width=2)
        #             # mazeCanvas.create_line(x+(charsize/2), y+charsize, x+charsize, y+charsize, width=2)
        #         x += charsize/2
        #         #create a vertical line to close off the right wall
        #     print
        #     x = 15
        # mazeCanvas.create_line((maze.width*charsize)/2, 10, (maze.width*charsize)/2, (maze.height*charsize)+10, width=2)
        # mazeCanvas.create_line(15, (maze.height*charsize)+10, (maze.width*charsize)/2, (maze.height*charsize)+10, width=2)
    
###########################################################################
##  Program file processing functions
###########################################################################

#this opens a text file for a maze
def openMaze():
    fileName = tkf.askopenfilename()
    if (len(fileName) > 0 and fileName != ""):
        global maze
        maze = mazeText(fileName)
        drawMaze()
        global forward
        colorSpot((maze.getGoalPosition()), forward)


###########################################################################
##  Program GUI setup
###########################################################################

#gui setup
root = Tk()

root.title("Path Finder")

#this holds everything
mainframe = Frame(root)
mainframe.pack(expand=YES, fill=BOTH)

#this is the panel for controlling the maze + pathfinder
controlPanel = Frame(mainframe)
toggleDisplayButton = Button(controlPanel, text="Toggle display", command = lambda: toggleDisplay())
loadButton = Button(controlPanel, text="Load...", command = lambda: openMaze())
dfsButton = Button(controlPanel, text="DFS", command = lambda: dfs())
bfsButton = Button(controlPanel, text="BFS", command = lambda: bfs())
aStarButton = Button(controlPanel, text="A*", command = lambda: aStar())
closestButton = Button(controlPanel, text="Closest", command = lambda: closest())
controlPanel.pack(side=TOP)
#toggleDisplayButton.pack(side=LEFT) #this isn't ready
loadButton.pack(side=LEFT)
dfsButton.pack(side=LEFT)
bfsButton.pack(side=LEFT)
aStarButton.pack(side=LEFT)
closestButton.pack(side=LEFT)

#this is the frame for the maze display
mazeFrame = Frame(mainframe)
mazeDisplay = ScrolledText(mazeFrame, wrap=NONE, state=DISABLED, bg="#FFF", fg="#000")#, height=28, width=80)
mazeCanvas = Canvas(mazeFrame, bg="#FFF")
mazeFrame.pack(side=BOTTOM, expand=YES, fill=BOTH)
mazeDisplay.pack(expand=YES, fill=BOTH)

if __name__ == "__main__":
    root.mainloop()
