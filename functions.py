from random import randint


def getValidActions(world, x, y, has_block):
    directions = ['north', 'south', 'west', 'east']
    state_action = world[(x, y)]['action']
    state_blocks = world[(x, y)]['no_of_blocks']
    validActions = []

    if has_block:
        if state_action == "d" and state_blocks < 4: return ["d"]
        for d in directions:
            if world[(x, y)][d] != 'nan':
                validActions.append(d)
        return validActions
    # does not have block
    if state_action == "p" and state_blocks > 0: return ["p"]
    for d in directions:
        if world[(x, y)][d] != 'nan':
            validActions.append(d)
    return validActions

def getNextCoords(action, world, x, y):
    if (action == 'd' or action == 'p'): return [x, y]
    return world[(x, y)][action]

def chooseRandomAction(valid_actions):
    if (valid_actions[0] == "d"): return ["d", 13]
    if (valid_actions[0] == "p"): return ["p", 13]
    index = randint(0, len(valid_actions) - 1)
    return [valid_actions[index], -1]


def actionToIndex(action):
    if action == 'north': n = 0
    elif action == 'south': n = 1
    elif action == 'east': n = 2
    elif action == 'west': n = 3
    elif action == 'p': n = 4
    elif action == 'd': n = 5
    else: return print("actionNumber recieved invalid action: '" + str(action) + "'")
    return n

def coordsNotValid(x, y, w, h):
    if x > w or x < 0 or y > h or y < 0:
        print('coords are out of bound')
        return True

def getStates(w, h):
    rows, cols = (h, w)
    matrix=[]
    count = 0
    for i in range(rows):
        col = []
        for j in range(cols):
            col.append(count)
            count += 1
        matrix.append(col)
    return matrix

# probablly gonna make something better 
# (update: i did, see 'getStates')
def getStateFromCoords(x, y):
    '''
    if (x == 0):
        if (y == 0 ): return 0
        if (y == 1 ): return 1
        if (y == 2 ): return 2
        if (y == 3 ): return 3
        if (y == 4 ): return 4
    if (x == 1):
        if (y == 0 ): return 5
        if (y == 1 ): return 6
        if (y == 2 ): return 7
        if (y == 3 ): return 8
        if (y == 4 ): return 9
    if (x == 2):
        if (y == 0 ): return 10
        if (y == 1 ): return 11
        if (y == 2 ): return 12
        if (y == 3 ): return 13
        if (y == 4 ): return 14
    if (x == 3):
        if (y == 0 ): return 15
        if (y == 1 ): return 16
        if (y == 2 ): return 17
        if (y == 3 ): return 18
        if (y == 4 ): return 19
    if (x == 4):
        if (y == 0 ): return 20
        if (y == 1 ): return 21
        if (y == 2 ): return 22
        if (y == 3 ): return 23
        if (y == 4 ): return 24
    '''
    return x * 5 + y
