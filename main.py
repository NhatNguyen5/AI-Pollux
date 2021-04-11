import time
import numpy as np
from functions import * 
from random import randint
from Visualize.visualize import Visualize as vl
from WorldProcessing.readWorld import ReadWorld

global x
global y
global drop_off_loc
global pick_up_loc
global has_block
global world

x = 0
y = 0
drop_off_loc = [(0, 0), (4, 0), (2, 2), (4, 4)]
pick_up_loc = [(1, 3), (4, 2)]
has_block = False
h, w, world = ReadWorld().fill_world('testworld.txt')


def getNextCoords(action):
    global world
    if (action == 'd' or action == 'p'): return [x, y]
    return world[(x, y)][action]

def applyAction(action):
    global x
    global y
    global drop_off_loc
    global pick_up_loc
    global has_block
    global world
    if action == 'd':
        world[(x, y)]['no_of_blocks'] += 1
        if world[(x, y)]['no_of_blocks'] == 4:
            drop_off_loc.remove((x, y))
            print((x, y), 'is full')
            time.sleep(1)
        has_block = False
    elif action == 'p':
        world[(x, y)]['no_of_blocks'] -= 1
        if world[(x, y)]['no_of_blocks'] == 0:
            pick_up_loc.remove((x, y))
            print((x, y), 'is empty')
            time.sleep(1)
        has_block = True

def actionNumber(action):
    n = 0
    if action == 'north':
        n = 0
    elif action == 'south':
        n = 1
    elif action == 'west':
        n = 2
    elif action == 'east':
        n = 3
    elif action == 'p':
        n = 4
    elif action == 'd':
        n = 5
    return n

def updateQTable(q_table, world, x, y, reward, alpha, gamma, action, app_op):
    q_values_future_state = []
    i = 0
    for a in app_op:
        i = actionNumber(a)
        q_values_future_state.append(q_table[world[(x, y)][a]][i])
    n = actionNumber(action)
    q_table[x, y][n] = (1 - alpha)*q_table[x, y][n] + alpha*(reward + gamma*max(q_values_future_state))


def main():
    global x
    global y
    global drop_off_loc
    global pick_up_loc
    global has_block
    global world

    next_x = -1
    next_y = -1
    FIRST_STEPS = 50
    SECOND_STEPS = 5500

    policy = "PRANDOM"
    # policy = "PEXPLOIT"
    # policy = "PGREEDY"

    # offset is diffence in q_table between row for a state, and the row for the same state when holding a block 
    q_offset = w * h
    q_size = q_offset * 2
    q_table = np.zeros((q_size, 6))

    print('Hello')
    world_vl = vl()
    world_vl.visualize_gen(h, w, world)

    for r in range(h):
        for c in range(w):
            if world[(c, r)]['action'] == 'd':
                world_vl.fill_block(world[(c, r)]['coor'], 'green')
            if world[(c, r)]['action'] == 'p':
                world_vl.fill_block(world[(c, r)]['coor'], 'blue')
            world_vl.write_block(world[(c, r)]['coor'], world[(c, r)]['action'], 'white')
            world_vl.write_block(world[(c, r)]['coor'], str(world[(c, r)]['coor']), 'black', 'n', 15)


    # q_table = np.zeros((w*2, h, 6))
    action = ['n', 's', 'w', 'e', 'p', 'd']


    q_table[x+1, 2] = 2
    q_table[(x+2), 3] = 3
    print(q_table)
    return


    world_vl.fill_block(world[(x, y)]['coor'], 'yellow')
    world_vl.write_block(world[(x, y)]['coor'], 'start', 'black')

    # always use PRANDOM for first 500 steps
    for i_d in range(0, FIRST_STEPS):
        print(i_d, '{:.2f}%'.format((i_d / FIRST_STEPS)*100))
        print('location: ', x, y)

        # check for out of bound values
        if x > max(world)[0] or x < 0 or y > max(world)[1] or y < 0:
            print('Out of bound')
            break

        # list of all possible operations at current state
        valid_actions = getValidActions(world, x, y, has_block)

        # choose action based off policy
        action, reward = chooseRandomAction(valid_actions)
        # action, reward = chooseExploitAction(valid_actions)
        # action, reward = chooseGreedyAction(valid_actions)
        print("action:", action)

        applyAction(action)
        next_x, next_y = getNextCoords(action)

        # update qtable

        

        x = next_x
        y = next_y

        world_vl.fill_block(world[(x, y)]['coor'], 'red')
        world_vl.write_block(world[(x, y)]['coor'], str(i_d), pos='s')
        # print("reward:", reward)

        # if terminal state reached
        if len(pick_up_loc) == 0 and len(drop_off_loc) == 0:
            break

    for r in range(h):
        for c in range(w):
            if world[(c, r)]['action'] == 'd':
                world_vl.fill_block(world[(c, r)]['coor'], 'green')
                world_vl.write_block(world[(c, r)]['coor'], str(world[(c, r)]['no_of_blocks']), 'black', pos='s')
            if world[(c, r)]['action'] == 'p':
                world_vl.fill_block(world[(c, r)]['coor'], 'blue')
                world_vl.write_block(world[(c, r)]['coor'], str(world[(c, r)]['no_of_blocks']), 'black', pos='s')
            world_vl.write_block(world[(c, r)]['coor'], world[(c, r)]['action'], 'white')
            world_vl.write_block(world[(c, r)]['coor'], str(world[(c, r)]['coor']), 'black', 'n', 15)



    # apply 'step' aka action
    # set new_state and reward from that state


# chose policy for next 5500 steps
# for _ in range(0, SECOND_STEPS):


# action = np.argmax(q_table[state, :])
# for e in world[(0, 0)]:
#     print(world[(0, 0)][e])


if __name__ == '__main__':
    main()

