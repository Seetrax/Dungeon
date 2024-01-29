import gui
import os
import re
import sys
import argparse
from grading import grading

###The arguments that can be changed through terminal given as arg parsers###########################################################
args={'q':'q1'}
parser = argparse.ArgumentParser(description="Manage the args for the game")
parser.add_argument("-q", type=str, help="question number to be evaluated")
args2 = parser.parse_args()
if args2.q :
    args['q']=args2.q

answer = grading(args)
