#  our own logic file. 

"""
In logicPlan.py, you will implement logic planning methods.
"""

from logic import conjoin, disjoin
from logic import PropSymbolExpr, Expr, to_cnf, pycoSAT, parseExpr, pl_true
from typing import Dict, List, Tuple, Callable, Generator, Any
import util

# Expr class is in logic.py . 

# QUESTION 1 ------------------------------------------------------------

def sentence1() -> Expr:
    """Returns a Expr instance that encodes that the following expressions are all true.
    
    A or B
    (not A) if and only if ((not B) or C)
    (not A) or (not B) or C
    """
    "*** BEGIN YOUR CODE HERE ***"

    """Write the sentences and then return them conjoined"""

    A = Expr("A")
    B = Expr("B")
    C = Expr("C")

    a_or_b = disjoin(A, B)
    expr2 = ~A % disjoin(~B, C)
    expr3 = disjoin(~A, ~B, C)

    return conjoin(a_or_b, expr2, expr3)
    "*** END YOUR CODE HERE ***"

def sentence2() -> Expr:
    """Returns a Expr instance that encodes that the following expressions are all true.
    
    C if and only if (B or D)
    A implies ((not B) and (not D))
    (not (B and (not C))) implies A
    (not D) implies C
    """
    "*** BEGIN YOUR CODE HERE ***"

    """Write the sentences and then return them conjoined"""

    A = Expr("A")
    B = Expr("B")
    C = Expr("C")
    D = Expr("D")

    expr1 = C % disjoin(B, D)
    expr2 = A >> conjoin(~B, ~D)
    expr3 = ~conjoin(B, ~C) >> A
    expr4 = ~D >> C

    return conjoin(expr1, expr2, expr3, expr4)
    "*** END YOUR CODE HERE ***"

def sentence3() -> Expr:
    """Using the symbols BaahubaliAlive_1 BaahubaliAlive_0, BaahubaliBorn_0, and BaahubaliKilled_0,
    created using the PropSymbolExpr constructor, return a PropSymbolExpr
    instance that encodes the following English sentences (in this order):

    Baahubali is alive at time 1 if and only if Baahubali was alive at time 0 and it was
    not killed at time 0 or it was not alive at time 0 and it was born at time 0.

    Baahubali cannot both be alive at time 0 and be born at time 0.

    Baahubali is born at time 0.
    (Project update: for this question only, [0] and _t are both acceptable.)
    """
    "*** BEGIN YOUR CODE HERE ***"

    """Make the sentences that are described and return them conjoined"""

    BaahubaliAlive_0 = PropSymbolExpr("BaahubaliAlive", 0)
    BaahubaliAlive_1 = PropSymbolExpr("BaahubaliAlive", 1)
    BaahubaliBorn_0 = PropSymbolExpr("BaahubaliBorn", 0)
    BaahubaliKilled_0 = PropSymbolExpr("BaahubaliKilled", 0)

    expr1 = BaahubaliAlive_1 % disjoin(conjoin(BaahubaliAlive_0, ~BaahubaliKilled_0), conjoin(~BaahubaliAlive_0, BaahubaliBorn_0))
    expr2 = ~conjoin(BaahubaliAlive_0, BaahubaliBorn_0)
    expr3 = BaahubaliBorn_0

    return conjoin(expr1, expr2, expr3)
    "*** END YOUR CODE HERE ***"

def findModel(sentence: Expr) -> Dict[Expr, bool]:
    """Given a propositional logic sentence (i.e. a Expr instance), returns a satisfying
    model if one exists. Otherwise, returns False.
    """
    cnf_sentence = to_cnf(sentence)
    return pycoSAT(cnf_sentence)

def entails(premise: Expr, conclusion: Expr) -> bool:
    """Returns True if the premise entails the conclusion and False otherwise.
    """
    "*** BEGIN YOUR CODE HERE ***"
    
    """If findModel doesn't find any model where the premise & not(conxlusion) is satisfiable return False"""

    return findModel(premise & ~conclusion) == False
    "*** END YOUR CODE HERE ***"

def plTrueInverse(assignments: Dict[Expr, bool], inverse_statement: Expr) -> bool:
    """Returns True if the (not inverse_statement) is True given assignments and False otherwise.
    pl_true may be useful here; see logic.py for its description.
    """
    "*** BEGIN YOUR CODE HERE ***"
    return pl_true(~inverse_statement, assignments)
    "*** END YOUR CODE HERE ***"

# QUESTION2 ------------------------------------------------------------------------

def atLeastOne(literals: List[Expr]) -> Expr:
    """
    Given a list of Expr literals (i.e. in the form A or ~A), return a single 
    Expr instance in CNF (conjunctive normal form) that represents the logic 
    that at least one of the literals  ist is true.
    >>> A = PropSymbolExpr('A');
    >>> B = PropSymbolExpr('B');
    >>> symbols = [A, B]
    >>> atleast1 = atLeastOne(symbols)
    >>> model1 = {A:False, B:False}
    >>> print(pl_true(atleast1,model1))
    False
    >>> model2 = {A:False, B:True}
    >>> print(pl_true(atleast1,model2))
    True
    >>> model3 = {A:True, B:True}
    >>> print(pl_true(atleast1,model2))
    True
    """
    "*** BEGIN YOUR CODE HERE ***"
    return disjoin(literals)
    "*** END YOUR CODE HERE ***"


def atMostOne(literals: List[Expr]) -> Expr:
    """
    Given a list of Expr literals, return a single Expr instance in 
    CNF (conjunctive normal form) that represents the logic that at most one of 
    the expressions in the list is true.
    itertools.combinations may be useful here.
    """
    "*** BEGIN YOUR CODE HERE ***"

    """Take all the combinations of 2 literals and disjoin them with not"""

    combinations = itertools.combinations(literals, 2)
    clauses_list = []
    for combo in combinations:
        clauses_list.append(disjoin(~combo[0], ~combo[1])) 
    
    return conjoin(clauses_list)
    "*** END YOUR CODE HERE ***"


def exactlyOne(literals: List[Expr]) -> Expr:
    """
    Given a list of Expr literals, return a single Expr instance in 
    CNF (conjunctive normal form)that represents the logic that exactly one of 
    the expressions in the list is true.
    """
    "*** BEGIN YOUR CODE HERE ***"
    # Use the previous functions
    return conjoin(atLeastOne(literals), atMostOne(literals))
    "*** END YOUR CODE HERE ***"

#---------------------  QUESTION 3  ----------------------------
'''
Knowledge Base
1.	Lion, Pit not in currentCell

Premises
1.	If roar in currentCell then lion in exactly one of the adjacent cell
2.	If breeze in currentCell then pit in atleast one of the adjacent cell.

Encode these statements : 
    Agent's current position does not have any wumpus or pit. 
    If agent recieves roar, it means that at exactly one of the adjacent position a lion is there. 
    If agent recieves breeze, it means that there is a pit on atlease one of the unexplored adjacent nodes. 
    explored nodes have no danger. 

have variables roar_current, lion_current, lion_up, lion_down, lion_left, lion_right, 
pit_current, pit_up, pit_down, pit_left, pit_right, breezy_current. 

'''
def question3() -> Expr:
    roar_current = Expr("Roar_current")
    lion_current = Expr("Lion_current")
    lion_up = Expr("Lion_up")
    lion_down = Expr("Lion_down")
    lion_left = Expr("Lion_left")
    lion_right = Expr("Lion_right")
    pit_current = Expr("Pit_current")
    pit_up = Expr("Pit_up")
    pit_down = Expr("Pit_down")
    pit_left = Expr("Pit_left")
    pit_right = Expr("Pit_right")
    breezy_current = Expr("Breezy_current")

    a = conjoin(~lion_current, ~pit_current)
    """
    roar_current => exactlyOne(lion_up, lion_down, lion_left, lion_right)
    disjoin(roar_current, exactlyOne([lion_up, lion_down, lion_left, lion_right]))
    """
    b = disjoin(roar_current, exactlyOne([lion_up, lion_down, lion_left, lion_right]))
    '''
    disjoin(breezy_current, atleastOne([lion_up, lion_down, lion_left, lion_right]))
    '''
    c = disjoin(breezy_current, atleastOne([lion_up, lion_down, lion_left, lion_right]))

    return conjoin(a, b, c)

class knowledgeBase:

    def __init__(self, gameState):
        pass

    def isLionHere(self, gameState):
        pass

    def isPitHere(self, gameState):
        pass

    def isRoarHere(self, gameState):
        pass

    def isBreezeHere(self, gameState):
        pass


























'''
# each square as an object 
# adjacency relation 
# better : squares as list 
# square topology list
# assuming length is 4 and breadth is 4

# squares
Square11 = PropSymbolExpr("Squares", 1, 1)
Square12 = PropSymbolExpr("Squares", 1, 2)
Square13 = PropSymbolExpr("Squares", 1, 3)
Square14 = PropSymbolExpr("Squares", 1, 4)

Square21 = PropSymbolExpr("Squares", 2, 1)
Square22 = PropSymbolExpr("Squares", 2, 2)
Square23 = PropSymbolExpr("Squares", 2, 3)
Square24 = PropSymbolExpr("Squares", 2, 4)

Square31 = PropSymbolExpr("Squares", 3, 1)
Square32 = PropSymbolExpr("Squares", 3, 2)
Square33 = PropSymbolExpr("Squares", 3, 3)
Square34 = PropSymbolExpr("Squares", 3, 4)

Square41 = PropSymbolExpr("Squares", 4, 1)
Square42 = PropSymbolExpr("Squares", 4, 2)
Square43 = PropSymbolExpr("Squares", 4, 3)
Square44 = PropSymbolExpr("Squares", 4, 4)

def dungeonphysicsAxioms(t: int, all_coords: List[Tuple], sensorModel: Callable = None, successorAxioms: Callable = None) -> Expr:
    """
    Given:
        t: timestep
        all_coords: list of (x, y) coordinates of the entire problem
        sensorModel(t, non_outer_wall_coords) -> Expr: function that generates
            the sensor model axioms. If None, it's not provided, so shouldn't be run.
        successorAxioms(t, walls_grid, non_outer_wall_coords) -> Expr: function that generates
            the sensor model axioms. If None, it's not provided, so shouldn't be run.
    Return a logic sentence containing all of the following:
        - for all (x, y) in all_coords:
            If a wall is at (x, y) --> dungeon is not at (x, y)
        - dungeon is at exactly one of the squares at timestep t.
        - dungeon takes exactly one action at timestep t.
        - Results of calling sensorModel(...), unless None.
        - Results of calling successorAxioms(...), describing how dungeon can end in various
            locations on this time step. Consider edge cases. Don't call if None.
    """
    dungeonphysics_sentences = []

    "*** BEGIN YOUR CODE HERE ***"

    # for x, y in all_coords:
    #    dungeonphysics_sentences.append(PropSymbolExpr(wall_str, x, y) >> ~PropSymbolExpr(dungeon_str, x, y, time=t))
    
    list_dungeon = []
    for x, y in all_coords:
        list_dungeon.append(PropSymbolExpr(dungeon_str, x, y, time=t))    
    dungeonphysics_sentences.append(exactlyOne(list_dungeon))

    list_actions = []
    for action in DIRECTIONS:
        list_actions.append(PropSymbolExpr(action, time=t))        
    dungeonphysics_sentences.append(exactlyOne(list_actions))

    if sensorModel != None:
        dungeonphysics_sentences.append(sensorModel(t, all_coords)/pacphysics/dungeonphysics

    
    if t > 0:
        if successorAxioms != None:
            dungeonphysics_sentences.append(successorAxioms(t, walls_grid, non_outer_wall_coords))
    
    return conjoin(dungeonphysics_sentences)
    "*** END YOUR CODE HERE ***"

 implement the basic DungeonPhysics
'''
















'''
# -------------------------------------------------------------------
# we are making some boxes

class Logic:
	def __init__(self, n, m):
		self.length = n
		self.width = m
		self.constantsDict = {SAFE  : 0, STINK : 1, ROAR : 2, LION : 3, PIT : 4}
		self.matrix = List()
		for i in range(n):
			l = List()
			for j in range(m):
				l.append([])
			self.matrix.append(l)
		self.matrix[0][0].append(SAFE)
		self.arena = self.world
	
'''
