# autograder.py
# -------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).

# imports from python standard library
import grading
import imp
import optparse
import os
import re
import sys
import csv
import projectParams
import random
random.seed(0)
try: 
    from pacman import GameState
except:
    pass

# register arguments and set default values
def readCommand(argv):
    args = dict()
    parser = optparse.OptionParser(description = 'Run public tests on student code')
    parser.set_defaults(generateSolutions=False, edxOutput=False, gsOutput=False, muteOutput=False, printTestCase=False, noGraphics=False)
    parser.add_option('--test-directory',
                      dest = 'testRoot',
                      default = 'test_cases',
                      help = 'Root test directory which contains subdirectories corresponding to each question')
    parser.add_option('--student-code',
                      dest = 'studentCode',
                      default = projectParams.STUDENT_CODE_DEFAULT,
                      help = 'comma separated list of student code files')
    parser.add_option('--code-directory',
                    dest = 'codeRoot',
                    default = "",
                    help = 'Root directory containing the student and testClass code')
    parser.add_option('--test-case-code',
                      dest = 'testCaseCode',
                      default = projectParams.PROJECT_TEST_CLASSES,
                      help = 'class containing testClass classes for this project')
    parser.add_option('--generate-solutions',
                      dest = 'generateSolutions',
                      action = 'store_true',
                      help = 'Write solutions generated to .solution file')
    parser.add_option('--edx-output',
                    dest = 'edxOutput',
                    action = 'store_true',
                    help = 'Generate edX output files')
    parser.add_option('--gradescope-output',
                    dest = 'gsOutput',
                    action = 'store_true',
                    help = 'Generate GradeScope output files')
    parser.add_option('--mute',
                    dest = 'muteOutput',
                    action = 'store_true',
                    help = 'Mute output from executing tests')
    parser.add_option('--print-tests', '-p',
                    dest = 'printTestCase',
                    action = 'store_true',
                    help = 'Print each test case before running them.')
    parser.add_option('--test', '-t',
                      dest = 'runTest',
                      default = None,
                      help = 'Run one particular test.  Relative to test root.')
    parser.add_option('--question', '-q',
                    dest = 'gradeQuestion',
                    default = None,
                    help = 'Grade one particular question.')
    parser.add_option('--no-graphics',
                    dest = 'noGraphics',
                    action = 'store_true',
                    help = 'No graphics display for pacman games.')
    (options, args) = parser.parse_args(argv)
    # args2 = parser.parse_args(argv)
    # if args2.question : args['method'] = 
    print(options)
    return options


# confirm we should author solution files
def confirmGenerate():
    print('WARNING: this action will overwrite any solution files.')
    print('Are you sure you want to proceed? (yes/no)')
    while True:
        ans = sys.stdin.readline().strip()
        if ans == 'yes':
            break
        elif ans == 'no':
            sys.exit(0)
        else:
            print('please answer either "yes" or "no"')


# TODO: Fix this so that it tracebacks work correctly
# Looking at source of the traceback module, presuming it works
# the same as the intepreters, it uses co_filename.  This is,
# however, a readonly attribute.
def setModuleName(module, filename):
    functionType = type(confirmGenerate)
    classType = type(optparse.Option)

    for i in dir(module):
        o = getattr(module, i)
        if hasattr(o, '__file__'): continue

        if type(o) == functionType:
            setattr(o, '__file__', filename)
        elif type(o) == classType:
            setattr(o, '__file__', filename)
            # TODO: assign member __file__'s?
        #print(i, type(o))


#from cStringIO import StringIO

def loadModuleString(moduleSource):
    # Below broken, imp doesn't believe its being passed a file:
    #    ValueError: load_module arg#2 should be a file or None
    #
    #f = StringIO(moduleCodeDict[k])
    #tmp = imp.load_module(k, f, k, (".py", "r", imp.PY_SOURCE))
    tmp = imp.new_module(k)
    exec(moduleCodeDict[k] in tmp.__dict__)
    setModuleName(tmp, k)
    return tmp

import py_compile

def loadModuleFile(moduleName, filePath):
    with open(filePath, 'r') as f:
        return imp.load_module(moduleName, f, "%s.py" % moduleName, (".py", "r", imp.PY_SOURCE))


def readFile(path, root=""):
    "Read file from disk at specified path and return as string"
    with open(os.path.join(root, path), 'r') as handle:
        return handle.read()


#######################################################################
# Error Hint Map
#######################################################################

# TODO: use these
ERROR_HINT_MAP = {
  'q1': {
    "<type 'exceptions.IndexError'>": """
      We noticed that your project threw an IndexError on q1.
      While many things may cause this, it may have been from
      assuming a certain number of successors from a state space
      or assuming a certain number of actions available from a given
      state. Try making your code more general (no hardcoded indices)
      and submit again!
    """
  },
  'q3': {
      "<type 'exceptions.AttributeError'>": """
        We noticed that your project threw an AttributeError on q3.
        While many things may cause this, it may have been from assuming
        a certain size or structure to the state space. For example, if you have
        a line of code assuming that the state is (x, y) and we run your code
        on a state space with (x, y, z), this error could be thrown. Try
        making your code more general and submit again!

    """
  }
}

import pprint

def splitStrings(d):
    d2 = dict(d)
    for k in d:
        if k[0:2] == "__":
            del d2[k]
            continue
        if d2[k].find("\n") >= 0:
            d2[k] = d2[k].split("\n")
    return d2


def printTest(testDict, solutionDict):
    pp = pprint.PrettyPrinter(indent=4)
    print("Test case:")
    for line in testDict["__raw_lines__"]:
        print("   |", line)
    print("Solution:")
    for line in solutionDict["__raw_lines__"]:
        print("   |", line)


def runTest(testName, moduleDict, printTestCase=False, display=None):
    import testParser
    import testClasses
    for module in moduleDict:
        setattr(sys.modules[__name__], module, moduleDict[module])

    testDict = testParser.TestParser(testName + ".test").parse()
    solutionDict = testParser.TestParser(testName + ".solution").parse()
    test_out_file = os.path.join('%s.test_output' % testName)
    testDict['test_out_file'] = test_out_file
    testClass = getattr(projectTestClasses, testDict['class'])

    questionClass = getattr(testClasses, 'Question')
    question = questionClass({'max_points': 0}, display)
    testCase = testClass(question, testDict)

    if printTestCase:
        printTest(testDict, solutionDict)

    # This is a fragile hack to create a stub grades object
    grades = grading.Grades(projectParams.PROJECT_NAME, [(None,0)])
    testCase.execute(grades, moduleDict, solutionDict)


# returns all the tests you need to run in order to run question
def getDepends(testParser, testRoot, question):
    allDeps = [question]
    questionDict = testParser.TestParser(os.path.join(testRoot, question, 'CONFIG')).parse()
    if 'depends' in questionDict:
        depends = questionDict['depends'].split()
        for d in depends:
            # run dependencies first
            allDeps = getDepends(testParser, testRoot, d) + allDeps
    return allDeps

# get list of questions to grade
def getTestSubdirs(testParser, testRoot, questionToGrade):
    problemDict = testParser.TestParser(os.path.join(testRoot, 'CONFIG')).parse()
    if questionToGrade != None:
        questions = getDepends(testParser, testRoot, questionToGrade)
        if len(questions) > 1:
            print('Note: due to dependencies, the following tests will be run: %s' % ' '.join(questions))
        return questions
    if 'order' in problemDict:
        return problemDict['order'].split()
    return sorted(os.listdir(testRoot))


# evaluate student code
def evaluate(generateSolutions = None, testRoot = None, moduleDict = dict(), exceptionMap=ERROR_HINT_MAP,
             edxOutput=False, muteOutput=False, gsOutput=False,
            printTestCase=False, questionToGrade=None, display=None):
    # imports of testbench code.  note that the testClasses import must follow
    # the import of student code due to dependencies
    # testParser is a class containing methods removeComments, parse - (parse test cases ig) and a property path. 
    '''
    import testParser
    import testClasses
    '''
    # testClasses contains class Question, some classes for various types of Questions and class TestCase which is a template modelling a generic test case

    # moduleDict is a list contains 'Search' and 'projectTestClasses'. 
    # projectTestClasses === searchTestClasses
    # searchTestClasses contain classes of GraphSearch, parseHeuristic, graphSearchTest, PacmanSearchTest, getStatesFromPath, CornerProblemsTest, HeuristicTest, HeuristicGrade, ClosestDotTest, 
    # CornerHeuristicSanity and CornerHeuristicPacman. 
    '''
    for module in moduleDict:
        setattr(sys.modules[__name__], module, moduleDict[module])
    
    questions = []
    questionDicts = {}
    '''
    # test_subdirs = ['q1']
    '''
    test_subdirs = getTestSubdirs(testParser, testRoot, questionToGrade)
    for q in test_subdirs:
        # subdir_path = 'test_cases/q1'
        subdir_path = os.path.join(testRoot, q)
        if not os.path.isdir(subdir_path) or q[0] == '.':
            continue

        # create a question object
        questionDict = testParser.TestParser(os.path.join(subdir_path, 'CONFIG')).parse()
	# questionDict contains the following : 
	# {'__raw_lines__': ['max_points: "3"', 'class: "PassAllTestsQuestion"', ''], 'path': 'test_cases/q1/CONFIG', '__emit__': [('oneline', 'max_points'), ('oneline', 'class'), ('raw', '')], 'max_points': '3', 'class': 'PassAllTestsQuestion'}

        questionClass = getattr(testClasses, questionDict['class'])
        # questionClass is an instance of class PassAllTestQuestions in testClasses
        question = questionClass(questionDict, display)
        questionDicts[q] = questionDict
        
        """
        questionDicts[q] contain the following : 
        {'__raw_lines__': ['max_points: "3"', 'class: "PassAllTestsQuestion"', ''], 'path': 'test_cases/q1/CONFIG', '__emit__': [('oneline', 'max_points'), ('oneline', 'class'), ('raw', '')], 'max_points': '3', 'class': 'PassAllTestsQuestion'}
        """
        # config contain maxpoints and PassAllTestsClass. 

        # load test cases into question
        tests = filter(lambda t: re.match('[^#~.].*\.test\Z', t), os.listdir(subdir_path))
        tests = map(lambda t: re.match('(.*)\.test\Z', t).group(1), tests)
	# tests is something, which if we iterate through it, we get tests we have to perform. In this, 
	# we are doing graph_backtrack, graph_bfs_vs_dfs, graph_infninite, graph_manypaths and pacman_1. We have to replace pacman_1 with something
        for t in sorted(tests):
            # path to the test_file
            test_file = os.path.join(subdir_path, '%s.test' % t)
	    # path to the solution_file
            solution_file = os.path.join(subdir_path, '%s.solution' % t)
	    # test_out_file is the path to the file to which test probably writes out test output to a test. 
            test_out_file = os.path.join(subdir_path, '%s.test_output' % t)
	    # parsed test_file is stored in testDict. 
	    # The things in .test file is stored as it is in testDict...
            testDict = testParser.TestParser(test_file).parse()
            
	    # if .test file contains 'disabled' or 'false', then the test is not performed. 
            if testDict.get("disabled", "false").lower() == "true":
                continue
            
            # saves file to which test output is written is saved in dict
            testDict['test_out_file'] = test_out_file
            
            # testClass is class for evaluation. eg : <class 'searchTestClasses.GraphSearchTest'>
            testClass = getattr(projectTestClasses, testDict['class'])
	    # question : <testClasses.PassAllTestsQuestion object at 0x101dfab90
            testCase = testClass(question, testDict)
            def makefun(testCase, solution_file):
                # in this search generateSolutions = False for all tests. 
                if generateSolutions:
                    # write solution file to disk
                    return lambda grades: testCase.writeSolution(moduleDict, solution_file)
                else:
                    # read in solution dictionary and pass as an argument
                    # same testDict
                    testDict = testParser.TestParser(test_file).parse()
                    # print solutionDict
                    solutionDict = testParser.TestParser(solution_file).parse()
                    # printTestCase is false. 
                    if printTestCase:
                        return lambda grades: printTest(testDict, solutionDict) or testCase.execute(grades, moduleDict, solutionDict)
                    else:
                        # returning function <function evaluate.<locals>.makefun.<locals>.<lambda> at 0x104354cc0>
                        return lambda grades: testCase.execute(grades, moduleDict, solutionDict)
            # question.addTestCase is None. 
            question.addTestCase(testCase, makefun(testCase, solution_file))


        # Note extra function is necessary for scoping reasons
        def makefun(question):
            return lambda grades: question.execute(grades)
        setattr(sys.modules[__name__], q, makefun(question))
        questions.append((q, question.getMaxPoints()))
    '''
    # grades object is grades object in grading.py
    print('before grade')
    grades = grading.Grades(projectParams.PROJECT_NAME, question,
                            gsOutput=gsOutput, edxOutput=edxOutput, muteOutput=muteOutput)
    print('after grade')
    print(grades)
    from pprint import pprint
    pprint(vars(grades))
    # questionToGrade = 'q1'
    '''
    if questionToGrade == None:
        for q in questionDicts:
            for prereq in questionDicts[q].get('depends', '').split():
                grades.addPrereq(q, prereq)
   '''

    # till now it seems the question is not being evaluated. 
    # sys.modules[__name__] is the gradingModule : the module with all grading functions. 
    # grades.grade(sys.modules[__name__], bonusPic = projectParams.BONUS_PIC)
    print('grades.grade()')
    grades.grade()
    print('I am out of grades')
    print(grades.points)
    return grades.points



def getDisplay(graphicsByDefault, options=None):
    graphics = graphicsByDefault
    if options is not None and options.noGraphics:
        graphics = False
    if graphics:
        try:
            import graphicsDisplay
            return graphicsDisplay.PacmanGraphics(1, frameTime=.05)
        except ImportError:
            pass
    import textDisplay
    return textDisplay.NullGraphics()



if __name__ == '__main__':
    print('Hello')
    options = readCommand(sys.argv)   
    question = str(options.gradeQuestion)
    method = None
    f = open("currentQuestion.csv",'w')
    wr = csv.writer(f, delimiter = ',')
    wr.writerow(['Question'])
    wr.writerow([question])
    # row = csv.reader(f)
    # for i in row:
    #     if question == i[0]:
    #        method = i[1]
    #        break
    f.close()
    # print(question)
    # print(method)
    """
    # options is a dictionary consist of values of all the arguments. 
    # when autograder.py -q q1 is called : the dict is 
    {'generateSolutions': False, 'edxOutput': False, 'gsOutput': False, 'muteOutput': False, 
    'printTestCase': False, 'noGraphics': False, 'testRoot': 'test_cases', 'studentCode': 'Search.py', 
   'codeRoot': '', 'testCaseCode': 'searchTestClasses.py', 'runTest': None, 'gradeQuestion': 'q1'}
    """
    
    # leave this if code
    # if options.generateSolutions:
    #     confirmGenerate()

    # codePaths = ['Search.py']
    # codePaths = options.studentCode.split(',')
    # codePaths = ['Search.py']
    
    # already commented code
    """
    # moduleCodeDict = {}
    # for cp in codePaths:
    #     moduleName = re.match('.*?([^/]*)\.py', cp).group(1)
    #     moduleCodeDict[moduleName] = readFile(cp, root=options.codeRoot)
    # moduleCodeDict['projectTestClasses'] = readFile(options.testCaseCode, root=options.codeRoot)
    # moduleDict = loadModuleDict(moduleCodeDict)
    """

    # moduleDict = {}
    # for cp in codePaths:
        # cp = 'Search.py'
	# moduleName = 'Search'
        # moduleName = re.match('.*?([^/]*)\.py', cp).group(1)
        # moduleDict[moduleName] = loadModuleFile(moduleName, os.path.join(options.codeRoot, cp))
	# currently codeRoot is empty string. 
    # moduleName = re.match('.*?([^/]*)\.py', options.testCaseCode).group(1)
    # moduleName = 'searchTestClasses'
    # moduleDict['projectTestClasses'] = loadModuleFile(moduleName, os.path.join(options.codeRoot, options.testCaseCode))
    # {'Search': <module 'Search' from '/Users/amithabh_a/Desktop/OELP/Dungeon/Search/Search.py'>, 'projectTestClasses': <module 'searchTestClasses' from '/Users/amithabh_a/Desktop/OELP/Dungeon/Search/searchTestClasses.py'>}

    # projectTestClasses : searchTestClasses
    # searchTestClasses contain classes of GraphSearch, parseHeuristic, graphSearchTest, PacmanSearchTest, getStatesFromPath, CornerProblemsTest, HeuristicTest, HeuristicGrade, ClosestDotTest, 
    # CornerHeuristicSanity and CornerHeuristicPacman. 

    # options.runTest = None
    # if options.runTest != None:
    #    runTest(options.runTest, moduleDict, printTestCase=options.printTestCase, display=getDisplay(True, options))
    # else:
    #evaluate(options.generateSolutions, options.testRoot, moduleDict,
    #        gsOutput=options.gsOutput,
    #        edxOutput=options.edxOutput, muteOutput=options.muteOutput, printTestCase=options.printTestCase,
    #        questionToGrade=options.gradeQuestion, display=getDisplay(options.gradeQuestion!=None, options))
    evaluate()
