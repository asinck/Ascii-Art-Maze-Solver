Ascii Art Maze Solver

This takes an ascii art maze as input, and solves it.

##There are currently four search algorithms inplemented:
* DFS, which does a depth-first search of the maze to find the solution.
* BFS, which does a breadth-first search of the maze to find the solution.
* A*, which expands the search node with the minimum path cost + heuristic estimate.
* Closest, which expands the search node closest to the goal.

##More Details:
###DFS:
This algorithm will go down as far as it can in the tree representation of the maze. In simpler terms, it will take all the left turns it can, then backtrack one turn and go down the center trail, and then backtrack and go down the right path, then backtrack twice and repeat the process. If this algorithm gets lucky, it will go directly to the goal. If it doesn't, it could end up going through most or all of the maze before finding the goal. This algorithm doesn't care about finding the shortest path to the goal, but makes an attempt to find the solution quickly.

###BFS:
This algorithm will search each point in the maze ordered by "walking distance" from the start. This is the same as checking each possible path in parallel. This typically takes longer to find the solution because it's checking all paths, but it is guaranteed to find the shortest path from the start to the goal.

###A*
A UCS (Uniform Cost Search) would will search down the path that has the lowest total cost to traverse. Because the mazes don't have path costs, this is approximately equivalent to a BFS. This algorithm is also guaranteed to find the shortest path from the start to the goal, but doesn't necessarily find that path quickly.

An A* search is similar to a UCS, except that it factors in a heuristic for how far that path is from the goal. For a given path, the estimated cost of that path is the total cost so far (the "walking distance" to that point) plus the estimated "walking distance" back. The heuristic used for estimating the "walking distance" back is the manhattan distance (for (x1, y1) and (x2, y2), the manhattan distance is abs(x1-x2) + abs(y1-y2)). A* will go down the path that has the lowest estimated cost. 

The A* is also guaranteed to find the shortest path from the start to the goal, but also doesn't necessarily find that path quickly.


###Closest
This is an algorithm I made myself (not that I invented it, of course) that goes down the path with the lowest estimated distance to the goal (the lowest heuristic). This is similar to a DFS, but instead of expanding the nodes in a set order (eg, left to right) it expands them in order of heuristic.

This algorithm is optimized for finding a solution quickly, but doesn't care about finding an optimal solution. This algorithm is not guaranteed to be faster in finding a solution though; for instance, if it chooses a path with a good heuristic that leads only to dead ends, it will need to backtrack all the way back up to take a path with a worse heuristic but that (hopefully) leads to the goal. 

--
This program was inspired by my AI class, and the UC Berkeley AI project, at http://ai.berkeley.edu .
