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
BFSsuccess = "#550055"

#this holds the text representation of the maze. It can work with the
#text to decide legal moves, where the goal position is, etc.
class mazeText():
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
        


    #this gets the valid moves from a position
    def getValidMoves(self, (x, y)):
        #the current position can't be on or outside boundary walls
        
        #note that height is downwards

        #because the left wall and top line are defined by
        #underscores, valid values begin at position (2, 2) and
        #run to (self.width-1, self.height-1)
        
        #note also that arrays and strings are 0 based, but self.width
        #and self.height are not
        
        if (x >= self.width or y >= self.height or x <= 0 or y <= 0):
            return []
        else:
            moves = []
            #North: y+1, x
            #East:  y, x+1
            #South: y-1, x
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

            # print "moves from", (x, y), ":", moves
            return moves

    #return the manhattan distance to the goal
    def manHeuristic(self, (x, y)):
        (goalX, goalY) = self.getGoalPosition()
        return abs(goalX - x) + abs(goalY - y)

    def eucHeuristic(self, (x, y)):
        import math
        (goalX, goalY) = self.getGoalPosition()
        return math.sqrt(math.pow((goalX - x), 2) + math.pow((goalY - y), 2))
    
    #return if the position is the goal
    def isGoal(self, (x, y)):
        return (x == self.width-1 and y == self.height-1)

    #return the position of the goal
    def getGoalPosition(self):
        return (self.width-1, self.height-1)

    #return a text representation of the maze
    def getText(self):
        return "\n".join(self.maze)

    
#notDone will give a message saying that that feature is not complete
def notDone(var=None):
    tkMessageBox.showinfo("Not Ready", "This feature is not complete yet.")


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

#this does a dfs of the maze for the solution
def dfs():
    if (maze == None):
        return

    resetMaze()
    #a list of positions visited already
    dejavu = []
    
    start = (1, 1)
    
    global path, forward, back

    colorSpot(start, forward)
    
    #if we're done, then we're done
    if (maze.isGoal(start)):
        return

    import time
    #this is the recursive DFS function
    def solve(position):
        
        moves = maze.getValidMoves(position)
        colorSpot(position, path)
        #time.sleep(maze.moveTime)
        for move in moves:
            found = False
            if move not in dejavu:
                dejavu.append(move)
                colorSpot(move, forward)
                time.sleep(maze.moveTime)
                if maze.isGoal(move):
                    return True
                else:
                    if (solve(move)):
                        return True
                colorSpot(move, back)
                time.sleep(maze.moveTime)
        return False

    #call the recursive function
    solve(start)


def bfs():
    if (maze == None):
        return
    resetMaze()
    
    class Node:
        def __init__(self, _node):
            self.path = []
            self.node = _node

    dejavu = []
    start = (1, 1)

    global path, forward, back

    colorSpot(start, forward)

    #if we're done, then we're done
    if (maze.isGoal(start)):
        return

    startNode = Node(start)
    import time
    def solve(queue):
        time.sleep(maze.moveTime)
        #time.sleep(maze.moveTime)
        nextLevel = []
        
        if (len(queue) == 0):
            return []
        for position in queue:
            colorSpot(position.node, path)
            #check if goal
            if maze.isGoal(position.node):
                return position.path
            else:
                
                #Go through the children of the current node, and for
                #each one, check if it's been visited. If not, add it
                #to the array of nodes that need to be checked the
                #next pass.
                children = maze.getValidMoves(position.node)
                if (len(children) == 1): # there will always be at least one: the parent
                    colorSpot(position.node, back)
                for child in children:
                    if (child not in dejavu):
                        dejavu.append(child)
                        colorSpot(child, forward)
                        node = Node(child)
                        node.path = position.path + [child]
                        if maze.isGoal(child):
                            return node.path
                        nextLevel.append(node)
        return solve(nextLevel)

    dejavu.append(start)
    solution = solve([startNode])
    if (len(solution) > 0):
        colorSpot(start, BFSsuccess)
        for spot in solution:
            time.sleep(maze.moveTime/2.0)
            colorSpot(spot, BFSsuccess)

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
    start = (1, 1)

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
            colorSpot(item.node, forward)
            time.sleep(maze.moveTime)
            if maze.isGoal(item.node):
                return item.path
            else:
                children = maze.getValidMoves(item.node)
                if (len(children) == 1): # there will always be at least one: the parent
                    colorSpot(item.node, back)
                else:
                    colorSpot(item.node, path)
                for child in children:
                    if (child not in dejavu):
                        if maze.isGoal(child):
                            return item.path + [child]

                        dejavu.append(child)
                        cost = item.cost + 1 #+1 because all steps cost 1
                        hcost = item.cost + heuristic(child)
                        node = Node(child, cost, hcost)
                        node.path = item.path + [child]
                        heapq.heappush(queue, node)

    solution = solve([startNode])
    if (len(solution) > 0):
        colorSpot(start, BFSsuccess)
        for spot in solution:
            time.sleep(maze.moveTime/2.0)
            colorSpot(spot, BFSsuccess)

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
    
    

#this opens a text file for a maze
def openMaze():
    fileName = tkf.askopenfilename()
    if (len(fileName) > 0 and fileName != ""):
        global maze
        maze = mazeText(fileName)
        drawMaze()
        colorSpot((maze.getGoalPosition()), "#0F0")

        
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
        colorSpot((maze.getGoalPosition()), "#0F0")


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
controlPanel.pack(side=TOP)
#toggleDisplayButton.pack(side=LEFT) #this isn't ready
loadButton.pack(side=LEFT)
dfsButton.pack(side=LEFT)
bfsButton.pack(side=LEFT)
aStarButton.pack(side=LEFT)

#this is the frame for the maze display
mazeFrame = Frame(mainframe)
mazeDisplay = ScrolledText(mazeFrame, wrap=NONE, state=DISABLED, bg="#FFF", fg="#000")#, height=28, width=80)
mazeCanvas = Canvas(mazeFrame, bg="#FFF")
mazeFrame.pack(side=BOTTOM, expand=YES, fill=BOTH)
mazeDisplay.pack(expand=YES, fill=BOTH)

if __name__ == "__main__":
    root.mainloop()
