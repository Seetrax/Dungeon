



## Introduction 

In this project, your Dungeon agent will find paths through his maze world, both to reach a particular location and to collect gold efficiently. You will build general search algorithms and apply them to Pacman scenarios.

This project includes an autograder for you to grade your answers on your machine. This can be run with the command:

```
python autograder.py
```

The code for this project consists of several Python files, some of which you will need to read and understand in order to complete the assignment, and some of which you can ignore. You can download all the code and supporting files as a zip archive.

Files you'll edit:
```search.py``` : 	Where all of your search algorithms will reside.

Files you might want to look at:
```game.py```
```util.py```	: Useful data structures for implementing search algorithms.
Supporting files you can ignore:
```autograder.py```
```Arguments.py```
```file_parser.py```
```grading.py```
```grid_label.py```
```human.py```
```Test.py```
```world.py```

## Welcome to Dungeons

After downloading the code (search.zip), unzipping it, and changing to the directory, you should be able to play a game of Pacman by typing the following at the command line:

```
python gui.py
```

Dungeon lives in a bushy cave of twisting corridors, deadly pits, fierce lions and glittering golds. Navigating this cave efficiently will be Dungeon’s first step in mastering his domain. 

For the search algorithm implementations in q1-3, you will implement the following roughly-written pseudocode for graph search:

```
Algorithm: GRAPH_SEARCH:
frontier = {startNode}
expanded = {}
while frontier is not empty:
    node = frontier.pop()
    if isGoal(node):
        return path_to_node
    if node not in expanded:
        expanded.add(node)
        for each child of node's children:
            frontier.push(child)
return failed
```

## Question 1 (3 points): Finding a Fixed Food Dot using Depth First Search

In ```search.py```, you’ll find a fully implemented SearchAgent, which plans out a path through Dungeon’s world and then executes that path step-by-step. The search algorithms for formulating a plan are not implemented. 

Now it’s time to write full-fledged generic search functions to help Dungeon plan routes!. Remember that a search node must contain not only a state but also the information necessary to reconstruct the path (plan) which gets to that state.

Important note: All of your search functions need to return a list of actions that will lead the agent from the start to the goal. These actions all have to be legal moves (valid directions, no moving through walls).

Important note: Make sure to use the Stack, Queue and PriorityQueue data structures provided to you in ```util.py```! These data structure implementations have particular properties which are required for compatibility with the autograder.

Hint: Each algorithm is very similar. Algorithms for DFS, BFS, UCS, and A* differ only in the details of how the frontier is managed. So, concentrate on getting DFS right and the rest should be relatively straightforward. Indeed, one possible implementation requires only a single generic search method which is configured with an algorithm-specific queuing strategy. (Your implementation need not be of this form to receive full credit).

Implement the depth-first search (DFS) algorithm in the depthFirstSearch function in search.py. To make your algorithm complete, write the graph search version of DFS, which avoids expanding any already visited states.

Your code should quickly find a solution for:

```
python dungeon.py -p agent -method dfs -graphics True -world Smallmaze.txt
```
```
python dungeon.py -p agent -method dfs -graphics True -world Medmaze.txt
```
```
python dungeon.py -p agent -method dfs -graphics True -world Bigmaze.txt
```

Grading: Please run the following command to see if your implementation passes all the autograder test cases.

```
python autograder.py -q q1
```

## Question 2 (3 points): Breadth First Search

̌̌Implement the breadth-first search (BFS) algorithm in the breadthFirstSearch function in ```Search.py```. Again, write a graph search algorithm that avoids expanding any already visited states. Test your code the same way you did for depth-first search.

```
python dungeon.py -p agent -method bfs -graphics True -world Medmaze.txt
```
```
python dungeon.py -p agent -method bfs -graphics True -world Bigmaze.txt
```

̌Does BFS find a least cost solution? If not, check your implementation.

Grading: Please run the following command to see if your implementation passes all the autograder test cases.

```
python autograder.py -q q2
```

## Question 3 (3 points): Uniform cost search

Implement  the Uniform cost search in ```Search.py```. 

You can test your ucs implementation on the original problem of finding a path through a maze to a fixed position. 

```
python dungeon.py -p agent -method ucs -graphics True -world Medmaze.txt
```
```
python dungeon.py -p agent -method ucs -graphics True -world Bigmaze.txt
```
Grading: Please run the following command to see if your implementation passes all the autograder test cases.

```
python autograder.py -q q3
```

## Question 4 (3 points): A* search

Implement A* graph search in the empty function aStarSearch in search.py. A* takes a heuristic function as an argument. Heuristics take two arguments: a state in the search problem (the main argument), and the problem itself (for reference information). 

You can test your A* implementation on the original problem of finding a path through a maze to a fixed position using the Manhattan distance heuristic (implemented already as manhattanHeuristic in searchAgents.py).

```
python dungeon.py -p agent -method astar -graphics True -world Medmaze.txt
```
```
python dungeon.py -p agent -method astar -graphics True -world Bigmaze.txt
```
Grading: Please run the following command to see if your implementation passes all the autograder test cases.

```
python autograder.py -q q4
```






