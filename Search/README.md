# Main Changes to Notice
* Analogy of Pacman's```search.py``` and ```searchAgents.py``` in Dungeons can be a single file. 
* ```mazes``` is renamed to ```layout```
* ```gui.py``` will be called in all instances where ```pacman.py``` is calld in Pacman
	* ```pacman.py``` in Pacman holds the logic for the classic pacman game along with the main code to run a game. Similarily ```gui.py``` in Dungeons holds the logic for the classic dungeon game along with the main code to run a game
* can't find ```search``` in ```search``` module and therefore ```SearchProblem```
* ```searchTestClasses.py``` line ```373``` ```from game import Actions``` is commented. 
* Wherever ````search.py``` and ```searchAgents.py``` having role with ```moduleDict```, change them to ```Search.py```. 
# Questions : 
* How autograder evaluated first four tests without even finishing the debugging in autograder? 
	* There are five tests, out of which fifth is tough. First debug fifth and then think about debugging others. 

# Getting information about the world 
* In Pacman, the arena is encoded using characters like ```%```. Some functions decode it and get the information about the walls and all. In Dungeons, the arena is specified by mentioning the wall positions explicitely.


## Major Changes done in autograder and related files to make Dungeons gradable

# In maze.py
* Commented ```from game import Grid``` in ```line 16``` since Grid's necessity didn't occur till now. 

* I am changing file names and then editing. 
