import numpy as np
from random import randint
import cv2 as cv
import time

from Visualize.visualize import Visualize as vl
from WorldProcessing.readWorld import ReadWorld


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


def getAppOps(world, x, y, has_block):
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


def chooseRandom(app_operators):
    if (app_operators[0] == "d"): return ["d", 13]
    if (app_operators[0] == "p"): return ["p", 13]
    index = randint(0, len(app_operators) - 1)
    return [app_operators[index], -1]


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
    print('Hello')
    alpha = 0.3
    gamma = 0.5
    h, w, world = ReadWorld().fill_world('testworld.txt')
    # print(world)
    # for b in world:
        # print(b, world[b]['east'])
    world_vl = vl()

    world_vl.visualize_gen(h, w, world)
    # fill_block((0, 0), 'green')
    # write_block((0, 0), 'Hello', 'white', 'n')
    # put_x((0, 0), 'white')

    for r in range(h):
        for c in range(w):
            if world[(c, r)]['action'] == 'd':
                world_vl.fill_block(world[(c, r)]['coor'], 'green')
            if world[(c, r)]['action'] == 'p':
                world_vl.fill_block(world[(c, r)]['coor'], 'blue')
            world_vl.write_block(world[(c, r)]['coor'], world[(c, r)]['action'], 'white')
            world_vl.write_block(world[(c, r)]['coor'], str(world[(c, r)]['coor']), 'black', 'n', 15)

    initial_state = (0, 0)

    # print(world[0, 1]['action'])
    q_table = np.zeros((w, h, 6))
    print(q_table)
    # action = ['n', 's', 'w', 'e', 'p', 'd']

    #  start episode

    FIRST_STEPS = 2000
    SECOND_STEPS = 5500
    policy = "PRANDOM"
    # policy = "PEXPLOIT"
    # policy = "PGREEDY"

    has_block = False
    x = 0
    y = 4
    world_vl.fill_block(world[(x, y)]['coor'], 'yellow')
    world_vl.write_block(world[(x, y)]['coor'], 'start', 'black')

    pick_up_loc = [(1, 3), (4, 2)]
    drop_off_loc = [(0, 0), (4, 0), (2, 2), (4, 4)]

    # always use PRANDOM for first 500 steps
    # i_d = 0
    for i_d in range(0, FIRST_STEPS):
    #while True:
        print(i_d, '{:.2f}%'.format((i_d / FIRST_STEPS)*100))
        print('location: ', x, y)
        if x > max(world)[0] or x < 0 or y > max(world)[1] or y < 0:
            print('Out of bound')
            break
        app_operators = getAppOps(world, x, y, has_block)
        # print('applicable_operators:', app_operators)

        chosen_op, reward = chooseRandom(app_operators)
        # updateQTable(q_table, world, )
        print("action:", chosen_op)
        if chosen_op == 'd':
            world[(x, y)]['no_of_blocks'] += 1
            if world[(x, y)]['no_of_blocks'] == 4:
                drop_off_loc.remove((x, y))
                print((x, y), 'is full')
                time.sleep(1)
            has_block = False
        elif chosen_op == 'p':
            world[(x, y)]['no_of_blocks'] -= 1
            if world[(x, y)]['no_of_blocks'] == 0:
                pick_up_loc.remove((x, y))
                print((x, y), 'is empty')
                time.sleep(1)
            has_block = True
        else:
            t_x = world[(x, y)][chosen_op][0]
            t_y = world[(x, y)][chosen_op][1]
            x = t_x
            y = t_y

        # print('next location: ', x, y)
        world_vl.fill_block(world[(x, y)]['coor'], 'red')
        world_vl.write_block(world[(x, y)]['coor'], str(i_d), pos='s')
        # print("reward:", reward)
        if len(pick_up_loc) == 0 and len(drop_off_loc) == 0:
            break
        # i_d += 1

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
    # updateQTable(q_table, world, x, y, reward, alpha, gamma, actions)
    print(q_table[0, 0])
    # apply 'step' aka chosen_op
    # set new_state and reward from that state


# chose policy for next 5500 steps
# for _ in range(0, SECOND_STEPS):


# action = np.argmax(q_table[state, :])
# for e in world[(0, 0)]:
#     print(world[(0, 0)][e])


if __name__ == '__main__':
    main()

