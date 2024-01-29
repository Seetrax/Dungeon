from game import GameState
from world import World
import Search
import os

def grading(args):
    files = ['Smallmaze.txt', 'Medmaze.txt', 'Bigmaze.txt']
    results = []
    student_solution = []
    autograder_solution = []
    for i in range(len(files)):
        world = World()
        world_path = os.path.join('mazes', files[i])
        world.generate_world(world_path)
        player_x=world.agent_col
        player_y=world.agent_row
        world.world[player_y][player_x].append('.')
        g = GameState(world)
        problem=Search.PosProblem(g,world,goal=(world.num_cols-1,world.num_rows-1))
        acts = 0
        solutions = {1:[['d', 'd', 'd', 'd', 'd', 'd', 'r', 'r', 'r', 'r', 'u', 'u', 'r', 'r', 'd', 'd'], ['r', 'r', 'r', 'r', 'd', 'd', 'd', 'd', 'r', 'r', 'r', 'r', 'u', 'u', 'l', 'l', 'u', 'u', 'r', 'r', 'r', 'r', 'd', 'd', 'd', 'd', 'd', 'd', 'r', 'r', 'r', 'r', 'd', 'd', 'd', 'd', 'l', 'l', 'l', 'l', 'd', 'd', 'l', 'l', 'u', 'u', 'l', 'l', 'u', 'u', 'u', 'u', 'l', 'l', 'l', 'l', 'd', 'd', 'r', 'r', 'd', 'd', 'l', 'l', 'd', 'd', 'r', 'r', 'r', 'r', 'd', 'd', 'r', 'r', 'r', 'r', 'r', 'r', 'u', 'u', 'r', 'r', 'd', 'd'], ['r', 'r', 'd', 'd', 'd', 'd', 'd', 'd', 'l', 'l', 'd', 'd', 'd', 'd', 'r', 'r', 'u', 'u', 'r', 'r', 'r', 'r', 'r', 'r', 'd', 'd', 'l', 'l', 'd', 'd', 'r', 'r', 'd', 'd', 'd', 'd', 'r', 'r', 'u', 'u', 'u', 'u', 'u', 'u', 'r', 'r', 'd', 'd', 'd', 'd', 'r', 'r', 'r', 'r', 'd', 'd', 'l', 'l', 'd', 'd', 'l', 'l', 'l', 'l', 'd', 'd', 'r', 'r', 'd', 'd', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r']] , 2: [['d', 'd', 'd', 'd', 'd', 'd', 'r', 'r', 'r', 'r', 'u', 'u', 'r', 'r', 'd', 'd'], ['r', 'r', 'r', 'r', 'd', 'd', 'd', 'd', 'r', 'r', 'r', 'r', 'u', 'u', 'l', 'l', 'u', 'u', 'r', 'r', 'r', 'r', 'd', 'd', 'd', 'd', 'd', 'd', 'r', 'r', 'r', 'r', 'd', 'd', 'd', 'd', 'l', 'l', 'l', 'l', 'd', 'd', 'l', 'l', 'u', 'u', 'l', 'l', 'u', 'u', 'u', 'u', 'l', 'l', 'l', 'l', 'd', 'd', 'r', 'r', 'd', 'd', 'l', 'l', 'd', 'd', 'r', 'r', 'r', 'r', 'd', 'd', 'r', 'r', 'r', 'r', 'r', 'r', 'u', 'u', 'r', 'r', 'd', 'd'], ['r', 'r', 'd', 'd', 'd', 'd', 'd', 'd', 'l', 'l', 'd', 'd', 'd', 'd', 'r', 'r', 'u', 'u', 'r', 'r', 'r', 'r', 'r', 'r', 'd', 'd', 'l', 'l', 'd', 'd', 'r', 'r', 'd', 'd', 'd', 'd', 'r', 'r', 'u', 'u', 'u', 'u', 'u', 'u', 'r', 'r', 'd', 'd', 'd', 'd', 'r', 'r', 'r', 'r', 'd', 'd', 'l', 'l', 'd', 'd', 'l', 'l', 'l', 'l', 'd', 'd', 'r', 'r', 'd', 'd', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r']] , 3 : [['d', 'd', 'd', 'd', 'd', 'd', 'r', 'r', 'r', 'r', 'u', 'u', 'r', 'r', 'd', 'd'], ['r', 'r', 'r', 'r', 'd', 'd', 'd', 'd', 'r', 'r', 'r', 'r', 'u', 'u', 'l', 'l', 'u', 'u', 'r', 'r', 'r', 'r', 'd', 'd', 'd', 'd', 'd', 'd', 'r', 'r', 'r', 'r', 'd', 'd', 'd', 'd', 'l', 'l', 'l', 'l', 'd', 'd', 'l', 'l', 'u', 'u', 'l', 'l', 'u', 'u', 'u', 'u', 'l', 'l', 'l', 'l', 'd', 'd', 'r', 'r', 'd', 'd', 'l', 'l', 'd', 'd', 'r', 'r', 'r', 'r', 'd', 'd', 'r', 'r', 'r', 'r', 'r', 'r', 'u', 'u', 'r', 'r', 'd', 'd'], ['r', 'r', 'd', 'd', 'd', 'd', 'd', 'd', 'l', 'l', 'd', 'd', 'd', 'd', 'r', 'r', 'u', 'u', 'r', 'r', 'r', 'r', 'r', 'r', 'd', 'd', 'l', 'l', 'd', 'd', 'r', 'r', 'd', 'd', 'd', 'd', 'r', 'r', 'u', 'u', 'u', 'u', 'u', 'u', 'r', 'r', 'd', 'd', 'd', 'd', 'r', 'r', 'r', 'r', 'd', 'd', 'l', 'l', 'd', 'd', 'l', 'l', 'l', 'l', 'd', 'd', 'r', 'r', 'd', 'd', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r']] , 4 : [['d', 'd', 'd', 'd', 'd', 'd', 'r', 'r', 'r', 'r', 'u', 'u', 'r', 'r', 'd', 'd'], ['r', 'r', 'r', 'r', 'd', 'd', 'd', 'd', 'r', 'r', 'r', 'r', 'u', 'u', 'l', 'l', 'u', 'u', 'r', 'r', 'r', 'r', 'd', 'd', 'd', 'd', 'd', 'd', 'r', 'r', 'r', 'r', 'd', 'd', 'd', 'd', 'l', 'l', 'l', 'l', 'd', 'd', 'l', 'l', 'u', 'u', 'l', 'l', 'u', 'u', 'u', 'u', 'l', 'l', 'l', 'l', 'd', 'd', 'r', 'r', 'd', 'd', 'l', 'l', 'd', 'd', 'r', 'r', 'r', 'r', 'd', 'd', 'r', 'r', 'r', 'r', 'r', 'r', 'u', 'u', 'r', 'r', 'd', 'd'] , ['r', 'r', 'd', 'd', 'd', 'd', 'd', 'd', 'l', 'l', 'd', 'd', 'd', 'd', 'r', 'r', 'u', 'u', 'r', 'r', 'r', 'r', 'r', 'r', 'd', 'd', 'l', 'l', 'd', 'd', 'r', 'r', 'd', 'd', 'd', 'd', 'r', 'r', 'u', 'u', 'u', 'u', 'u', 'u', 'r', 'r', 'd', 'd', 'd', 'd', 'r', 'r', 'r', 'r', 'd', 'd', 'l', 'l', 'd', 'd', 'l', 'l', 'l', 'l', 'd', 'd', 'r', 'r', 'd', 'd', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r']]}
        if(args['q'] == 'q1'):
            acts = Search.dfs(problem)
            if acts == solutions[1][i]:
                results.append(True)
            else:
                results.append(False)
            student_solution.append(acts)
            autograder_solution.append(solutions[1][i])
        elif(args['q'] == 'q2'):
            acts = Search.bfs(problem)
            if acts == solutions[2][i]:
                results.append(True)
            else:
                results.append(False)
            student_solution.append(acts)
            autograder_solution.append(solutions[2][i])
        elif(args['q'] == 'q3'):
            acts = Search.ucs(problem)
            if acts == solutions[3][i]:
                results.append(True)
            else:
                results.append(False)
            student_solution.append(acts)
            autograder_solution.append(solutions[3][i])
        elif(args['q'] == 'q4'):
            acts = Search.astar(problem)
            if acts == solutions[4][i]:
                results.append(True)
            else:
                results.append(False)
            student_solution.append(acts)
            autograder_solution.append(solutions[4][i])
    printSolution(results, student_solution, autograder_solution)

def printSolution(results, student_solution, autograder_solution):
    print("\nGRADING\n")
    totalPoints = 0
    studentPoints = 0
    for i in range(len(results)):
        totalPoints += 1
        print("TestCase ", i+1, " : ", end = "")
        if student_solution[i] == autograder_solution[i]:
            print("PASS")
            print()
            studentPoints += 1
        else:
            print("TestCase Failed! ")
            print("Your Solution : ", student_solution[i])
            print("autograder Solution : ", autograder_solution[i])
        print()
    print("\nGrading : ", studentPoints, "/",totalPoints, "\n")
