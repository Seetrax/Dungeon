# grading.py
# ----------
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


"Common code for autograders"

from html import escape
import time
import json
import traceback
from collections import defaultdict
import util
import sys
import csv

class Grades:
  "A data structure for project grades, along with formatting code to display them"
  def __init__(self, projectName = None, questionsAndMaxesList = None,
               gsOutput=False, edxOutput=False, muteOutput=False):
    """
    Defines the grading scheme for a project
      projectName: project name
      questionsAndMaxesDict: a list of (question name, max points per question)
    """
    # self.questions = [el[0] for el in questionsAndMaxesList]
    self.maxes = None
    self.method = None
    self.questionClass = None

    f = open('currentQuestion.csv', 'r')
    row = csv.reader(f)

    for i in row:
        self.question = i[0] 
    f.close()
    print(self.question)
    f = open('files.csv', 'r')
    row = csv.reader(f)
    next(row)
    for i in row:
        print(i[0])
        print(self.question)
        if int(i[0][2]) == int(self.question[1]):
            print('True')
            self.method = i[1]
            self.maxes = int(i[2])
            self.questionClass = i[3]
    f.close()
    print('maxes')
    print(self.maxes)
    print(self.method)
    print(self.questionClass)

    # self.maxes = dict(questionsAndMaxesList)
    self.points = Counter()
    # self.messages = { 'q1' : []}
    # self.messages = dict([(q, []) for q in self.questions])
    self.messages ={self.question: []}
    # self.project = projectName
    self.start = time.localtime()[1:6]
    # self.sane = True # Sanity checks
    # self.currentQuestion = None # Which question we're grading
    # following three lines set false
    self.edxOutput = edxOutput
    self.gsOutput = gsOutput  # GradeScope output
    self.mute = muteOutput
    self.prereqs = defaultdict(set)
    # defaultdict(<class 'set'>, {})

    #print('Autograder transcript for %s' % self.project)
    print('Starting on %d-%d at %d:%02d:%02d' % self.start)

  def addPrereq(self, question, prereq):
    self.prereqs[question].add(prereq)

  # def grade(self, gradingModule, exceptionMap = {}, bonusPic = False):
  def grade(self, gradingModule, exceptionMap = {}):
    """
    Grades each question
      gradingModule: the module with all the grading functions (pass in with sys.modules[__name__])
    """

    completedQuestions = set([])
    for q in [self.question]: # this listing of self.question is totally unwanted. 
      # q = 'q1'
      print('\nQuestion %s' % q)
      print('=' * (9 + len(q)))
      print
      self.currentQuestion = q

      incompleted = self.prereqs[q].difference(completedQuestions)
      if len(incompleted) > 0:
          prereq = incompleted.pop()
          print(
"""*** NOTE: Make sure to complete Question %s before working on Question %s,
*** because Question %s builds upon your answer for Question %s.
""" % (prereq, q, q, prereq))
          continue

      if self.mute: util.mutePrint()
      try:
        # this is an important line. 
        # print(getattr(gradingModule, q))
        # print('error potential line')
        # sys.exit(1)
	# the below line straight go to __call__ in class TimeoutFunction in util. 

        print('before important util')
        # util.TimeoutFunction(getattr(gradingModule, q),1800)(self) # Call the question's function
        # <function evaluate.<locals>.makefun.<locals>.<lambda> at 0x105560680>
        # util.TimeoutFunction(q,1800)(self) # Call the question's function
        print('after important util')
        # sys.exit(1)
        # print('error potential line over')
        # sys.exit(1)
        #TimeoutFunction(getattr(gradingModule, q),1200)(self) # Call the question's function
      except Exception as inst:
        self.addExceptionMessage(q, inst, traceback)
        self.addErrorHints(exceptionMap, inst, q[1])
      except:
        self.fail('FAIL: Terminated with a string exception.')
      finally:
        if self.mute: util.unmutePrint()

      if self.points[q] >= self.maxes:
        completedQuestions.add(q)

      print('\n### Question %s: %d/%d ###\n' % (q, self.points[q], self.maxes))


    print('\nFinished at %d:%02d:%02d' % time.localtime()[3:6])
    print("\nProvisional grades\n==================")

    for q in self.question:
      print('Question %s: %d/%d' % (q, self.points[q], self.maxes))
    print('------------------')
    # print('Total: %d/%d' % (self.points.totalCount(), sum(self.maxes.values())))
    print('Total: %d/%d' % (self.points.totalCount(), self.maxes))
    if self.points.totalCount() == 25:
      print("""

                     ALL HAIL GRANDPAC.
              LONG LIVE THE GHOSTBUSTING KING.

                  ---      ----      ---
                  |  \    /  + \    /  |
                  | + \--/      \--/ + |
                  |   +     +          |
                  | +     +        +   |
                @@@@@@@@@@@@@@@@@@@@@@@@@@
              @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
            @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
            @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
            \   @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
             \ /  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
              V   \   @@@@@@@@@@@@@@@@@@@@@@@@@@@@
                   \ /  @@@@@@@@@@@@@@@@@@@@@@@@@@
                    V     @@@@@@@@@@@@@@@@@@@@@@@@
                            @@@@@@@@@@@@@@@@@@@@@@
                    /\      @@@@@@@@@@@@@@@@@@@@@@
                   /  \  @@@@@@@@@@@@@@@@@@@@@@@@@
              /\  /    @@@@@@@@@@@@@@@@@@@@@@@@@@@
             /  \ @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
            /    @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
            @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
            @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
              @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
                @@@@@@@@@@@@@@@@@@@@@@@@@@
                    @@@@@@@@@@@@@@@@@@

""")
    print("""
Your grades are NOT yet registered.  To register your grades, make sure
to follow your instructor's guidelines to receive credit on your project.
""")

    if self.edxOutput:
        self.produceOutput()
    if self.gsOutput:
        self.produceGradeScopeOutput()

  def addExceptionMessage(self, q, inst, traceback):
    """
    Method to format the exception message, this is more complicated because
    we need to escape the traceback but wrap the exception in a <pre> tag
    """
    self.fail('FAIL: Exception raised: %s' % inst)
    self.addMessage('')
    for line in traceback.format_exc().split('\n'):
        self.addMessage(line)

  def addErrorHints(self, exceptionMap, errorInstance, questionNum):
    typeOf = str(type(errorInstance))
    questionName = 'q' + questionNum
    errorHint = ''

    # question specific error hints
    if exceptionMap.get(questionName):
      questionMap = exceptionMap.get(questionName)
      if (questionMap.get(typeOf)):
        errorHint = questionMap.get(typeOf)
    # fall back to general error messages if a question specific
    # one does not exist
    if (exceptionMap.get(typeOf)):
      errorHint = exceptionMap.get(typeOf)

    # dont include the HTML if we have no error hint
    if not errorHint:
      return ''

    for line in errorHint.split('\n'):
      self.addMessage(line)

  def produceGradeScopeOutput(self):
    out_dct = {}

    # total of entire submission
    total_possible = sum(self.maxes.values())
    total_score = sum(self.points.values())
    out_dct['score'] = total_score
    out_dct['max_score'] = total_possible
    out_dct['output'] = "Total score (%d / %d)" % (total_score, total_possible)

    # individual tests
    tests_out = []
    for name in self.questions:
      test_out = {}
      # test name
      test_out['name'] = name
      # test score
      test_out['score'] = self.points[name]
      test_out['max_score'] = self.maxes[name]
      # others
      is_correct = self.points[name] >= self.maxes[name]
      test_out['output'] = "  Question {num} ({points}/{max}) {correct}".format(
          num=(name[1] if len(name) == 2 else name),
          points=test_out['score'],
          max=test_out['max_score'],
          correct=('X' if not is_correct else ''),
      )
      test_out['tags'] = []
      tests_out.append(test_out)
    out_dct['tests'] = tests_out

    # file output
    with open('gradescope_response.json', 'w') as outfile:
        json.dump(out_dct, outfile)
    return

  def produceOutput(self):
    edxOutput = open('edx_response.html', 'w')
    edxOutput.write("<div>")

    # first sum
    total_possible = sum(self.maxes.values())
    total_score = sum(self.points.values())
    checkOrX = '<span class="incorrect"/>'
    if (total_score >= total_possible):
        checkOrX = '<span class="correct"/>'
    header = """
        <h3>
            Total score ({total_score} / {total_possible})
        </h3>
    """.format(total_score = total_score,
      total_possible = total_possible,
      checkOrX = checkOrX
    )
    edxOutput.write(header)

    for q in self.questions:
      if len(q) == 2:
          name = q[1]
      else:
          name = q
      checkOrX = '<span class="incorrect"/>'
      if (self.points[q] >= self.maxes[q]):
        checkOrX = '<span class="correct"/>'
      #messages = '\n<br/>\n'.join(self.messages[q])
      messages = "<pre>%s</pre>" % '\n'.join(self.messages[q])
      output = """
        <div class="test">
          <section>
          <div class="shortform">
            Question {q} ({points}/{max}) {checkOrX}
          </div>
        <div class="longform">
          {messages}
        </div>
        </section>
      </div>
      """.format(q = name,
        max = self.maxes[q],
        messages = messages,
        checkOrX = checkOrX,
        points = self.points[q]
      )
      # print("*** output for Question %s " % q[1])
      # print(output)
      edxOutput.write(output)
    edxOutput.write("</div>")
    edxOutput.close()
    edxOutput = open('edx_grade', 'w')
    edxOutput.write(str(self.points.totalCount()))
    edxOutput.close()

  def fail(self, message, raw=False):
    "Sets sanity check bit to false and outputs a message"
    self.sane = False
    self.assignZeroCredit()
    self.addMessage(message, raw)

  def assignZeroCredit(self):
    self.points[self.currentQuestion] = 0

  def addPoints(self, amt):
    self.points[self.currentQuestion] += amt

  def deductPoints(self, amt):
    self.points[self.currentQuestion] -= amt

  def assignFullCredit(self, message="", raw=False):
    self.points[self.currentQuestion] = self.maxes[self.currentQuestion]
    if message != "":
      self.addMessage(message, raw)

  def addMessage(self, message, raw=False):
    if not raw:
        # We assume raw messages, formatted for HTML, are printed separately
        if self.mute: util.unmutePrint()
        print('*** ' + message)
        if self.mute: util.mutePrint()
        message = escape(message)
    self.messages[self.currentQuestion].append(message)

  def addMessageToEmail(self, message):
    print("WARNING**** addMessageToEmail is deprecated %s" % message)
    for line in message.split('\n'):
      pass
      #print('%%% ' + line + ' %%%')
      #self.messages[self.currentQuestion].append(line)





class Counter(dict):
  """
  Dict with default 0
  """
  def __getitem__(self, idx):
    try:
      return dict.__getitem__(self, idx)
    except KeyError:
      return 0

  def totalCount(self):
    """
    Returns the sum of counts for all keys.
    """
    return sum(self.values())
