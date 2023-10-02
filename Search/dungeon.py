import gui
import os
import re
import sys
import argparse

###The arguments that can be changed through terminal given as arg parsers###########################################################
args={'world':'world.txt','omni':False,'player':'human','method':None,'graphics' : True}
parser = argparse.ArgumentParser(description="Manage the args for the game")
parser.add_argument("-method", type=str, help="change search method to any strategy")
parser.add_argument("-world", type=str, help="change maze config")
parser.add_argument("-omni", type=str, help="change omniscience of the agent")
parser.add_argument("-p", type=str, help="switch player from human to agent")
parser.add_argument("-graphics", type=str, help="set graphics for the game")
args2 = parser.parse_args()
if args2.method :
    args['method']=args2.method
    args['omni']=True
if args2.world :
    args['world']=args2.world

if args2.p :
    args['player']=args2.p
if args2.graphics :
    args['graphics']=args2.graphics
if args['graphics']==True:
    gui.game(args)

##elif args['graphics']==False:
    
