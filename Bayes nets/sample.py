def constructBayesNet(gameState):
    """
    Construct an empty Bayes net according to the structure given in Figure 1
    of the project description.

    You *must* name all variables using the constants in this function.

    In this method, you should:
    - populate `variables` with the Bayes Net nodes
    - populate `edges` with every edge in the Bayes Net. we will represent each
      edge as a tuple `(from, to)`.
    - set each `variableDomainsDict[var] = values`, where `values` is a list
      of the possible assignments to `var`.
        - each agent position is a tuple (x, y) where x and y are 0-indexed
        - each observed distance is a noisy Manhattan distance:
          it's non-negative and |obs - true| <= MAX_NOISE
    - this uses slightly simplified mechanics vs the ones used later for simplicity
    """
    # constants to use
    HUNTER_X_Y = "Hunter_x_y"
    LION_X+1_Y = "Lion_x+1_y"
    PIT_X_Y+1 = "Pit_x_y+1"
    ROAR_X_Y = "Roar_x_y"
    STINK_X_Y = "Stink_x_y"
    X_RANGE = gameState.getWalls().width
    Y_RANGE = gameState.getWalls().height
    MAX_NOISE = 7

    variables = []
    edges = []
    variableDomainsDict = {}

    "*** YOUR CODE HERE ***"
    variables=[HUNTER_X_Y,LION_X+1_Y,PIT_X_Y+1,ROAR_X_Y,STINK_X_Y]
    for i in variables:
        variableDomainsDict[i]=[]
    edges.append((LION_X+1_Y,ROAR_X_Y))
    edges.append((HUNTER_X_Y,ROAR_X_Y))
    edges.append((HUNTER_X_Y,STINK_X_Y))
    edges.append((PIT_X_Y+1,STINK_X_Y))
    lis0=[]
    lis1=[]
    for x in range(X_RANGE):
        for y in range(Y_RANGE):
            variableDomainsDict[HUNTER_X_Y].append((x,y))
            variableDomainsDict[LION_X+1_Y].append((x,y))
            variableDomainsDict[PIT_X_Y+1].append((x,y))
    for i in variableDomainsDict[HUNTER_X_Y]:
        for j in variableDomainsDict[LION_X+1_Y]:
            if (manhattanDistance(i,j))-MAX_NOISE<0:
                for l in range(0,(manhattanDistance(i,j))+MAX_NOISE+1):
                    if l not in lis0:
                        lis0.append(l)
            else:
                for l in range((manhattanDistance(i,j))-MAX_NOISE,(manhattanDistance(i,j))+MAX_NOISE+1):
                    if l not in lis0:
                        lis0.append(l)
            
    for i in variableDomainsDict[HUNTER_X_Y]:
        for j in variableDomainsDict[PIT_X_Y+1]:
            if (manhattanDistance(i,j))-MAX_NOISE<0:
                for l in range(0,(manhattanDistance(i,j))+MAX_NOISE+1):
                    if l not in lis1:
                        lis1.append(l)
            else:
                for l in range((manhattanDistance(i,j))-MAX_NOISE,(manhattanDistance(i,j))+MAX_NOISE+1):
                    if l not in lis1:
                        lis1.append(l)
    variableDomainsDict[ROAR_X_Y]=lis0
    variableDomainsDict[STINK_X_Y]=lis1
    #print(variableDomainsDict[OBS1])       
    #raiseNotDefined()
    "*** END YOUR CODE HERE ***"

    net = bn.constructEmptyBayesNet(variables, edges, variableDomainsDict)
    return net
