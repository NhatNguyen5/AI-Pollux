import numpy as np
from random import randint
# import cv2 as cv
import time
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


# World:
# world has blocks, which has 'coor'(it's coordinate), 'north', 'south', 'west', 'east'
# it's neighbor blocks(edges and corner will have some nan neighbors)
# and action(0 is nothing, 'd' is drop and 'p' is pick up,
# block and it's elements can be access with world[(x, y)]['key']

# Visualization:
# read_world(file_name) // read world from file
# fill_world(file_name) // fill a world dictionary
# visualize_gen(no_block_h, no_block_w, world) // Generate a picture
# fill_block((x, y), 'color') // fill block at x, y with color
# write_block((x, y), txt, 'color', 'pos') // write a color txt to block at x, y, pos in the block (n, s, w, e, c)
# put_x((x, y), 'color') // put a big X on the block


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

    q_table = np.zeros((w, h, 6))
    action = ['n', 's', 'w', 'e', 'p', 'd']

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

