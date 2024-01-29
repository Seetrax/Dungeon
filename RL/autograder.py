import ValueAgent
import QlearnAgent
import argparse
import os
import util

from world import World
Val_q1test1_w1 = util.Counter({(0, 0): -10.0, (0, 2): 0.0, (0, 3): 0.0, (1, 1): 0.0, (1, 2): 0.0, (1, 3): 0.0, (2, 0): 0.0, (2, 1): 0.0, (3, 1): 0.0, (3, 2): 10.0})
Val_q1test2_w1 = util.Counter({(0, 0): -10.0, (0, 2): 0.0, (0, 3): 0.0, (1, 1): 0.0, (1, 2): 0.0, (1, 3): 0.0, (2, 0): 0.0, (2, 1): 0.0, (3, 1): 9.0, (3, 2): 10.0})
Val_q1test3_w1 = util.Counter({(0, 0): -10.0, (0, 2): 0.0, (0, 3): 0.0, (1, 1): 7.29, (1, 2): 6.561, (1, 3): 0.0, (2, 0): 7.29, (2, 1): 8.1, (3, 1): 9.0, (3, 2): 10.0})
Val_q1test4_w1 = util.Counter({(0, 0): -10.0, (0, 2): 5.9, (0, 3): 5.31, (1, 1): 7.29, (1, 2): 6.56, (1, 3): 5.9, (2, 0): 7.29, (2, 1): 8.1, (3, 1): 9.0, (3, 2): 10.0})
q1_cases=[Val_q1test1_w1,Val_q1test2_w1,Val_q1test3_w1,Val_q1test4_w1]

Val_q2test1_w1=util.Counter({(0, 0): 'r', (0, 1): None, (0, 2): 'r', (0, 3): 'u', (1, 0): None, (1, 1): 'r', (1, 2): 'u', (1, 3): 'u', (2, 0): 'd', (2, 1): 'u', (2, 2): None, (2, 3): None, (3, 0): None, (3, 1): 'd', (3, 2): 'd', (3, 3): None})
Val_q2test2_w1=util.Counter({(0, 0): 'r', (0, 1): None, (0, 2): 'r', (0, 3): 'u', (1, 0): None, (1, 1): 'r', (1, 2): 'u', (1, 3): 'u', (2, 0): 'd', (2, 1): 'r', (2, 2): None, (2, 3): None, (3, 0): None, (3, 1): 'd', (3, 2): 'd', (3, 3): None})
Val_q2test3_w1=util.Counter({(0, 0): 'r', (0, 1): None, (0, 2): 'r', (0, 3): 'u', (1, 0): None, (1, 1): 'r', (1, 2): 'u', (1, 3): 'u', (2, 0): 'd', (2, 1): 'r', (2, 2): None, (2, 3): None, (3, 0): None, (3, 1): 'd', (3, 2): 'd', (3, 3): None})
Val_q2test4_w1=util.Counter({(0, 0): 'r', (0, 1): None, (0, 2): 'r', (0, 3): 'u', (1, 0): None, (1, 1): 'r', (1, 2): 'u', (1, 3): 'u', (2, 0): 'd', (2, 1): 'r', (2, 2): None, (2, 3): None, (3, 0): None, (3, 1): 'd', (3, 2): 'd', (3, 3): None})
q2_cases=[Val_q2test1_w1,Val_q2test2_w1,Val_q2test3_w1,Val_q2test4_w1]


args = {}

q=None
parser = argparse.ArgumentParser(description="question no")
parser.add_argument("-q", type=str, help="question")
grade=0
def print_grid(rows, columns,d):
    for i in range(0, rows ):
        for j in range(0, columns):
            print(d[(j,i)], end="\t")
        print()
def comp_int(d1,d2):
    for i in d1:
        if (abs(round(d1[i],2)-d2[i])>0.2):
            return False
    return True
def comp_str(d1,d2):
    for i in d1:
        if (d1[i]!=d2[i]):
            return False
    return True
def rou(d):
    d1=util.Counter()
    for i in d:
        d1[i]=round(d[i],2)
    return d1
def grader(q):
    global grade
    w_t1=os.path.join('mazes','world.txt')
    w_t2=os.path.join('mazes','world.txt')
    w_t3=os.path.join('mazes','world.txt')
    w_t4=os.path.join('mazes','world.txt')

    if q=='q1':
        args = {'world':os.path.join('mazes','world.txt'),'frames':10,'omni':True,'player':'agent','method':'valearn','graphics':False}
        world=World()
        world.generate_world(args['world'])
        it=[1,2,5,100]
        g1=0
        f=False
        print ("Question : 1")
        print ("========================================================")
        for i in range(4):
            wo=q1_cases[i]
            agent = ValueAgent.ValueIterAgent(world,omni=True,iterations=it[i])
            if not comp_int(agent.values,wo):
                print (f"Test {i+1} failed : \n")
                print ("Correct values : ",end="\n")
                print_grid(4,4,rou(wo))
                print()
                print ("Student values : ",end="\n")
                print_grid(4,4,rou(agent.values))
                f=True
                break
            else:
                print (f"Test {i+1} passed.")
        if f!=True:
            grade+=3
            g1+=3
        print ("========================================================")
        print(f"Score : {g1}/3")
    if q=='q2':
        args = {'world':os.path.join('mazes','world.txt'),'frames':10,'omni':True,'player':'agent','method':'valearn','graphics':False}
        world=World()
        world.generate_world(args['world'])
        it=[1,2,5,100]
        g1=0
        f=False
        print ("Question : 2")
        print ("========================================================")
        for i in range(4):
            wo=q2_cases[i]
            agent = ValueAgent.ValueIterAgent(world,omni=True,iterations=it[i])
            do={}
            for l in range(world.num_rows):
                for m in range(world.num_cols):
                    do[(l,m)]=agent.getAction((l,m))
            
            if not (comp_str(wo,do)):
                print (f"Test {i+1} failed : \n")
                print ("Correct values : ",end="\n")
                print_grid(4,4,wo)
                print()
                print ("Student values : ",end="\n")
                print_grid(4,4,do)
                f=True
                break
            else:
                print (f"Test {i+1} passed.")
        if f!=True:
            grade+=3
            g1+=3
        print ("========================================================")
        print(f"Score : {g1}/3")
    '''if q=='q1':
        args = {'world':os.path.join('mazes','world.txt'),'frames':10,'omni':True,'player':'agent','method':'valearn','graphics':False}
        world=World()
        world.generate_world(args['world'])
        agent = ValueAgent.ValueIterAgent(world,omni=True,iterations=1)
        if comp(agent.values,Val_q1test1_w1):
            grade+=3
        print(grade)
    if q=='q1':
        args = {'world':os.path.join('mazes','world.txt'),'frames':10,'omni':True,'player':'agent','method':'valearn','graphics':False}
        world=World()
        world.generate_world(args['world'])
        agent = ValueAgent.ValueIterAgent(world,omni=True,iterations=1)
        if comp(agent.values,Val_q1test1_w1):
            grade+=3
        print(grade)'''

args2 = parser.parse_args()
if args2.q :
    q=args2.q

if q!=None:
    grader(q)
    

