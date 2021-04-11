import time
import numpy as np
import random
from functions import * 
from vis_funcs import * 
from Visualize.visualize import Visualize as vl
from WorldProcessing.readWorld import ReadWorld

global x
global y
global drop_off_loc
global pick_up_loc
global has_block
global world

x = 0
y = 4
drop_off_loc = [(0, 0), (4, 0), (2, 2), (4, 4)]
pick_up_loc = [(1, 3), (4, 2)]
has_block = False
h, w, world = ReadWorld().fill_world('testworld.txt')

# states, given x and y, returns state for q_table
# access state with states[x][y]
states = getStates(w, h)

# offset is diffence in q_table between row for a state, and the row for the same state when holding a block 
q_offset = w * h
q_size = q_offset * 2
q_table = np.zeros((q_size, 6))

alpha = 0.5     # learning rate
gamma = 0.2     # discount rate
epsilon = 0.8   # chance of being greedy in exploit policy


def applyAction(action):
    global drop_off_loc
    global pick_up_loc
    global has_block
    global world
    if action == 'd':
        world[(x, y)]['no_of_blocks'] += 1
        if world[(x, y)]['no_of_blocks'] == 4:
            drop_off_loc.remove((x, y))
            print((x, y), 'is full')
        has_block = False
    elif action == 'p':
        world[(x, y)]['no_of_blocks'] -= 1
        if world[(x, y)]['no_of_blocks'] == 0:
            pick_up_loc.remove((x, y))
            print((x, y), 'is empty')
        has_block = True


def updateQTable(q_table, world, x, y, reward, alpha, gamma, action, app_op):
    q_values_future_state = []
    i = 0
    for a in app_op:
        i = actionNumber(a)
        q_values_future_state.append(q_table[world[(x, y)][a]][i])
    n = actionNumber(action)
    q_table[x, y][n] = (1 - alpha)*q_table[x, y][n] + alpha*(reward + gamma*max(q_values_future_state))

def Q(state, action):
    return (q_table[state][actionNumber(action)])

def bestValidAction(state, actions):
    max_val = -1
    bestAction = actions[0]
    for action in actions:
        val = q_table[state][actionNumber(action)]
        if val > max_val:
            max_val = val
            bestAction = action
    return bestAction

def maxQ(state, actions):
    bestAction = bestValidAction(state, actions)
    return q_table[state][actionNumber(bestAction)]


def exploitAction(state, valid_actions, epsilon):
    if (valid_actions[0] == "d"): return ["d", 13]
    if (valid_actions[0] == "p"): return ["p", 13]
    if (random.uniform(0, 1) > epsilon): 
        return chooseRandomAction(valid_actions)
    return [bestValidAction(state, valid_actions), -1]



def main():


    FIRST_STEPS = 500
    SECOND_STEPS = 5500
    global x
    global y
    global drop_off_loc
    global pick_up_loc
    global has_block
    global world

    done = False
    next_x = -1
    next_y = -1
    
    # policy = "PRANDOM"
    policy = "PEXPLOIT"
    # policy = "PGREEDY"

    # build world in starting state
    world_vl = vl()
    world_vl.visualize_gen(h, w, world)
    initWorld(h, w, world, world_vl, x, y)


    # always use PRANDOM for first 500 steps
    for step in range(0, FIRST_STEPS):
        print(step, '{:.2f}%'.format((step / (FIRST_STEPS+SECOND_STEPS))*100))

        # this "state" is used for q_table
        state = states[x][y]
        if (has_block): state += q_offset

        # list of all possible operations at current state
        valid_actions = getValidActions(world, x, y, has_block)
        
        action, reward = chooseRandomAction(valid_actions)
        print("action:", action)

        # has_block gets updated here
        applyAction(action)

        next_x, next_y = getNextCoords(action, world, x, y)
        next_valid_actions = getValidActions(world, next_x, next_y, has_block)        
        next_state = states[next_x][next_y]
        if (has_block): next_state += q_offset

        # update qtable  
        q_table[state][actionNumber(action)] = (1-alpha)*Q(state, action) + alpha*(reward + gamma*maxQ(next_state, next_valid_actions))

        # 'move' to the next state
        x = next_x
        y = next_y

        # if terminal state reached
        if len(pick_up_loc) == 0 and len(drop_off_loc) == 0:
            print("\nTerminal state reached")
            break

        # break if the next x or y is not valid (should never happen)
        if (coordsNotValid(x, y, w, h)): break


    for step in range(0, SECOND_STEPS):
        print(step, '{:.2f}%'.format(((step+FIRST_STEPS)/(FIRST_STEPS+SECOND_STEPS))*100))

        # this "state" is used for q_table
        state = states[x][y]
        if (has_block): state += q_offset

        # list of all possible operations at current state
        valid_actions = getValidActions(world, x, y, has_block)

        if (policy == 'PRANDOM'):
            action, reward = chooseRandomAction(valid_actions)
        elif (policy == 'PEXPLOIT'):
            action, reward = exploitAction(state, valid_actions, epsilon)
        elif (policy == 'PGREEDY'):
            action, reward = chooseRandomAction(valid_actions)
        print("action:", action)


        # has_block gets updated here
        applyAction(action)

        next_x, next_y = getNextCoords(action, world, x, y)
        next_valid_actions = getValidActions(world, next_x, next_y, has_block)        
        next_state = states[next_x][next_y]
        if (has_block): next_state += q_offset

        # update qtable  
        q_table[state][actionNumber(action)] = (1-alpha)*Q(state, action) + alpha*(reward + gamma*maxQ(next_state, next_valid_actions))

        # 'move' to the next state
        x = next_x
        y = next_y

        # if terminal state reached
        if len(pick_up_loc) == 0 and len(drop_off_loc) == 0:
            print("\nTerminal state reached")
            break

        # break if the next x or y is not valid (should never happen)
        if (coordsNotValid(x, y, w, h)): break


    updateWorld(h, w, world, world_vl)

    print(q_table)
    print("\ncompleted in", step+1, "steps")



if __name__ == '__main__':
    main()

