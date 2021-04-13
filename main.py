import time
import numpy as np
import random
from functions import *
from vis_funcs import *
from Visualize.visualize import Visualize as vl
from WorldProcessing.readWorld import ReadWorld
import cv2 as cv

FIRST_STEPS = 500
SECOND_STEPS = 5500
count_steps = 0
episode = 1

random.seed(random.uniform(1, 1000))

# global x,  y, drop_off_loc, pick_up_loc, has_block, done, world, q_offset, q_table

# build world in starting state
start_x = 0
start_y = 4
x = 0
y = 4
drop_off_loc = [(0, 0), (4, 0), (2, 2), (4, 4)]
pick_up_loc = [(1, 3), (4, 2)]
has_block = False
done = False
h, w, world = ReadWorld().fill_world('testworld.txt')

vis_objs = dict()

# states, given x and y, returns state index for q_table
# get index with states[x][y]
states = getStates(w, h)

# offset is diffence in q_table between row for a state, and the row for the same state when holding a block
q_offset = w * h
q_table = np.zeros((q_offset * 2, 6))

alpha = 0.3  # learning rate
gamma = 0.5  # discount rate
epsilon = 0.8  # chance of being greedy in exploit policy


def main():
    global world
    global episode
    # policy = "PRANDOM"
    policy = "PEXPLOIT"
    # policy = "PGREEDY"

    # visualizing world in starting state
    vis_objs['world_vl'] = vl('world')
    vis_objs['world_vl'].visualize_gen(h, w)
    initWorld(h, w, world, vis_objs['world_vl'], start_x, start_y)

    # always use PRANDOM for first 500 steps
    steps1 = doSteps(FIRST_STEPS, 'PRANDOM')

    vis_objs['q_table_no_block'] = vl('q_table_no_block')
    vis_objs['q_table_with_block'] = vl('q_table_with_block')

    vis_objs['agent_monitor'] = vl('agent_monitor')
    vis_objs['agent_monitor'].visualize_gen(h, w)
    initQTableWorld(h, w, world, vis_objs['agent_monitor'], start_x, start_y)
    updateQTableWorld(h, w, world, vis_objs['agent_monitor'], x, y)

    # print("q_table after 500 steps")
    # print(q_table)

    # if terminal state was not reached in first 500 steps, keep going
    steps2 = 0
    if (done == False):
        steps2 = doSteps(SECOND_STEPS, policy)

    print("\n\nq_table after completed")
    print(q_table)

    if not done:
        episode -= 1
    print("\ncompleted", episode, 'episodes in', steps1 + steps2, "steps")

    # update world
    updateWorld(h, w, world, vis_objs['world_vl'])
    # update final q_table with no block
    vis_objs['q_table_no_block'].visualize_gen(h, w)
    initQTableWorld(h, w, world, vis_objs['q_table_no_block'], start_x, start_y)
    updateQTableWorld(h, w, world, vis_objs['q_table_no_block'], x, y)
    fillQValues(h, w, q_table, vis_objs['q_table_no_block'], False)
    # update final q_table with block
    vis_objs['q_table_with_block'].visualize_gen(h, w)
    initQTableWorld(h, w, world, vis_objs['q_table_with_block'], start_x, start_y)
    updateQTableWorld(h, w, world, vis_objs['q_table_with_block'], x, y)
    fillQValues(h, w, q_table, vis_objs['q_table_with_block'], True)
    # update agent position
    if has_block:
        putAgent(h, w, q_table, world, vis_objs['q_table_with_block'], has_block, x, y, start_x, start_y, 'ab')
    else:
        putAgent(h, w, q_table, world, vis_objs['q_table_no_block'], has_block, x, y, start_x, start_y, 'a')


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


def bestValidAction(state, actions):
    max_val = -1
    bestAction = actions[0]
    for action in actions:
        val = q_table[state][actionToIndex(action)]
        # if two actions have the same val, pick a random one
        if (val == max_val):
            # 50% chance of not changing action
            if (random.uniform(0, 1) > 0.5): continue
            bestAction = action
        if val > max_val:
            max_val = val
            bestAction = action
    return bestAction


def Q(state, action):
    return (q_table[state][actionToIndex(action)])


def maxQ(state, actions):
    bestAction = bestValidAction(state, actions)
    return q_table[state][actionToIndex(bestAction)]


def exploitAction(state, valid_actions, epsilon):
    if (valid_actions[0] == "d"): return ["d", 13]
    if (valid_actions[0] == "p"): return ["p", 13]
    if (random.uniform(0, 1) > epsilon):
        return chooseRandomAction(valid_actions)
    return [bestValidAction(state, valid_actions), -1]


def greedyAction(state, valid_actions):
    if (valid_actions[0] == "d"): return ["d", 13]
    if (valid_actions[0] == "p"): return ["p", 13]
    return [bestValidAction(state, valid_actions), -1]


def doSteps(steps, policy):
    global x, y, drop_off_loc, pick_up_loc, has_block, done, world, q_offset, q_table, count_steps, episode

    step = 0
    ntw = True  # from no block to with block
    wtn = True  # from with block to no block

    for step in range(0, steps):
        # this "state" is used for q_table
        state = states[y][x]
        if (has_block): state += q_offset

        # list of all possible operations at current state
        valid_actions = getValidActions(world, x, y, has_block)

        action = ''
        reward = -1

        if (policy == 'PRANDOM'):
            action, reward = chooseRandomAction(valid_actions)
        elif (policy == 'PEXPLOIT'):
            action, reward = exploitAction(state, valid_actions, epsilon)
        elif (policy == 'PGREEDY'):
            action, reward = greedyAction(state, valid_actions)

        # has_block gets updated here
        applyAction(action)

        next_x, next_y = getNextCoords(action, world, x, y)
        if (coordsNotValid(next_x, next_y, w, h)): break
        next_valid_actions = getValidActions(world, next_x, next_y, has_block)
        next_state = states[next_y][next_x]
        if (has_block): next_state += q_offset

        # update qtable
        q_table[state][actionToIndex(action)] = \
            (1 - alpha) * Q(state, action) + alpha * (reward + gamma * maxQ(next_state, next_valid_actions))

        # keep track of prev state for step visualize part
        prev_x = x
        prev_y = y

        # 'move' to the next state
        x = next_x
        y = next_y

        # if terminal state reached
        # reset world, put agent back at start

        if len(pick_up_loc) == 0 and len(drop_off_loc) == 0:
            print('episode ', episode, 'is done | agent takes:', count_steps, 'steps')
            print("\nTerminal state reached")
            done = True
            x = 0
            y = 4
            drop_off_loc = [(0, 0), (4, 0), (2, 2), (4, 4)]
            pick_up_loc = [(1, 3), (4, 2)]
            has_block = False
            done = False
            _, _, world = ReadWorld().fill_world('testworld.txt')
            updateDropAndPickSpots(h, w, q_table, False,
                                   drop_off_loc, pick_up_loc, vis_objs['q_table_no_block'], world)
            updateDropAndPickSpots(h, w, q_table, True,
                                   drop_off_loc, pick_up_loc, vis_objs['q_table_with_block'], world)
            print('q_table:')
            print(q_table)
            print('-------------------------------------------------')
            # reset episode steps
            count_steps = 0
            # count episode
            episode += 1
            # break

        # break if the next x or y is not valid (should never happen)
        if (coordsNotValid(x, y, w, h)): break

        # count episode steps
        count_steps += 1

        # visualize each step
        watch = 0

        if steps != 500 and watch:
            print('\n' * 5)
            # print(q_table)
            print(valid_actions)
            print('action: {:5s}'.format(action), '| reward:', reward)
            print('ntw:', ntw, '| wtn:', wtn)
            if has_block:
                wtn = True
                if ntw:
                    vis_objs['agent_monitor'].visualize_gen(h, w)
                    initQTableWorld(h, w, world, vis_objs['agent_monitor'], start_x, start_y)
                    updateQTableWorld(h, w, world, vis_objs['agent_monitor'], x, y)
                    fillQValues(h, w, q_table, vis_objs['agent_monitor'], has_block)
                    ntw = False
                updateCell(h, w, q_table, world, vis_objs['agent_monitor'],
                           has_block, prev_x, prev_y, start_x, start_y)
                putAgent(h, w, q_table, world, vis_objs['agent_monitor'], has_block, x, y, start_x, start_y, 'ab')

            else:
                ntw = True
                if wtn:
                    vis_objs['agent_monitor'].visualize_gen(h, w)
                    initQTableWorld(h, w, world, vis_objs['agent_monitor'], start_x, start_y)
                    updateQTableWorld(h, w, world, vis_objs['agent_monitor'], x, y)
                    fillQValues(h, w, q_table, vis_objs['agent_monitor'], has_block)
                    wtn = False
                cv.destroyWindow('With block')
                updateCell(h, w, q_table, world, vis_objs['agent_monitor'],
                           has_block, prev_x, prev_y, start_x, start_y)
                putAgent(h, w, q_table, world, vis_objs['agent_monitor'], has_block, x, y, start_x, start_y, 'a')

            img = cv.imread('agent_monitor.png')
            cv.imshow('agent monitor', img)
            cv.waitKey(1)

    if step + 1 == SECOND_STEPS:
        print('episode ', episode, 'is not done | agent takes:', count_steps)
        print('6000 steps reached')
    return step + 1


if __name__ == '__main__':
    main()
