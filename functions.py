from random import randint
import time

def getValidActions(world, x, y, has_block):
    directions = ['north', 'south', 'west', 'east']
    return_ops = []

    if has_block:
        if world[(x, y)]['action'] == "d" and world[(x, y)]['no_of_blocks'] < 4:
            return_ops.append("d")
            print("DELIVERED! (", x, y, ') has', world[(x, y)]['no_of_blocks'] + 1, 'blocks')
            time.sleep(1)
            return return_ops
        else:
            for d in directions:
                if world[(x, y)][d] != 'nan':
                    return_ops.append(d)
                    
    # does not have block
    else:
        if world[(x, y)]['action'] == "p" and world[(x, y)]['no_of_blocks'] > 0:
            return_ops.append("p")
            print("PICKED UP! (", x, y, ') has', world[(x, y)]['no_of_blocks'] - 1, 'blocks left')
            time.sleep(1)
            return return_ops
        for d in directions:
            if world[(x, y)][d] != 'nan':
                return_ops.append(d)
    return return_ops

def chooseRandomAction(valid_actions):
    if (valid_actions[0] == "d"): return ["d", 13]
    if (valid_actions[0] == "p"): return ["p", 13]
    index = randint(0, len(valid_actions) - 1)
    return [valid_actions[index], -1]

def actionNumber(action):
    if action == 'north': n = 0
    if action == 'south': n = 1
    if action == 'west': n = 2
    if action == 'east': n = 3
    if action == 'p': n = 4
    if action == 'd': n = 5
    return n