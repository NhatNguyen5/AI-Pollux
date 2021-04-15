import time
import numpy as np
import random
from functions import *
from vis_funcs import *
from Visualize.visualize import Visualize as vl
from WorldProcessing.readWorld import ReadWorld
import cv2 as cv
import matplotlib.pyplot as plt
import pandas as pd
import openpyxl
from openpyxl.workbook import Workbook

FIRST_STEPS = 500
SECOND_STEPS = 5500
count_steps = 0
episode = 1

episode_list=[]
steps_count_list=[]
terminal_reached=[]

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

# smartanizer # EXPERIMENTAL FEATURE
'''
best_q_table = q_table  # EXPERIMENTAL FEATURE
best_steps = SECOND_STEPS  # EXPERIMENTAL FEATURE
best_episode = 0  # EXPERIMENTAL FEATURE
'''

alpha = 0.3  # learning rate
gamma = 0.5  # discount rate
epsilon = 0.8  # chance of being greedy in exploit policy

# BANK ACCOUNT (USE FOR MEASURING PERFORMANCE)
bank_plot_steps = np.arange(SECOND_STEPS)  # step array use for plotting
bank = []
bank_account = [0]
# put bank account in the bank
def regBankAccount():
    global bank_account
    bank.append(bank_account)
    bank_account = [0]
    print('Put episode', episode, 'account in the bank')

def plotPerformanceBank():
    plt.figure(1)
    max_len = []
    for ba in bank:
        max_len.append(len(ba))
    for i, ba in enumerate(bank):
        plt.plot(bank_plot_steps[:max(max_len)],
                 np.pad(ba, (0, max(max_len) - len(ba)),
                        'constant', constant_values=ba[len(ba) - 1]), label='e%d' % (i + 1))
    plt.xlabel('Steps')
    plt.ylabel('Accumulated reward')
    plt.legend()
    plt.savefig('performance_bank_plot.png')

# ----------------------------------------------------------

# DELIVERY STEPS (MEASURE PERFORMANCE)
delivery_plot_steps = np.arange(FIRST_STEPS + SECOND_STEPS)
delivery_steps = 0
prev_del_step = 0
num_of_blocks_delivered = 0
delivery_tracker = np.zeros(FIRST_STEPS + SECOND_STEPS)

def plotPerformanceDelSteps():
    plt.figure(2)
    curr_nob = 0
    last_pos = 0
    track = -1
    while delivery_tracker[track] != num_of_blocks_delivered: track -= 1
    for i in range(FIRST_STEPS + SECOND_STEPS + track, FIRST_STEPS + SECOND_STEPS):
        delivery_tracker[i] = num_of_blocks_delivered
    for i, n in enumerate(delivery_tracker):
        if curr_nob == 16:
            curr_nob = -1
        if n == curr_nob + 1:
            curr_nob += 1
            incre = 1/(i - last_pos)
            for j in range(last_pos + 1, i):
                delivery_tracker[j] = delivery_tracker[j-1] + incre
            last_pos = i

    plt.plot(delivery_plot_steps, delivery_tracker)
    plt.xlabel('Steps')
    plt.ylabel('Block delivered')
    plt.savefig('performance_del_steps_plot.png')
    
def output_to_exel(df_marks):
    writer = pd.ExcelWriter('output' + '.xlsx')
    # write dataframe to excel
    df_marks.to_excel(writer)
    # save the excel
    writer.save()
    print('DataFrame is written successfully to Excel File.')
# ----------------------------------------------------------

# 4th experiment enabler
fourth_expm = 0

# visualize each step
watch = 0

# GET USER INPUT
def getAcceptedInput(question, accepted_inputs, return_values):
    user_input = input(question)
    while not (user_input in accepted_inputs):
        print('Input not valid, try again!')
        user_input = input(question)
    else:
        return return_values[accepted_inputs.index(user_input)]


def main():
    # take user input
    global fourth_expm, watch, drop_off_loc, pick_up_loc
    default = getAcceptedInput("Use default (Q_LEARNING, PEXPLOIT, no monitor, plot)?\n(yes/no):",
                               ['yes', 'no'], [True, False])
    policy = ''
    if default:
        method = "Q_LEARNING"
        policy = "PEXPLOIT"
        watch = False
        plot = True
    else:
        method = getAcceptedInput("Which learning method?\n(Q_LEARNING/SARSA):",
                                  ["Q_LEARNING", "SARSA"], ["Q_LEARNING", "SARSA"])
        fourth_expm = getAcceptedInput("Enable fourth experiment?\n(yes/no):", ['yes', 'no'], [True, False])
        if not fourth_expm:
            policy = getAcceptedInput("Which policy?\n(PRANDOM/PEXPLOIT/PGREEDY):",
                                      ["PRANDOM", "PEXPLOIT", "PGREEDY"], ["PRANDOM", "PEXPLOIT", "PGREEDY"])
        watch = getAcceptedInput("Monitor agent?\n(yes/no):", ['yes', 'no'], [True, False])
        plot = getAcceptedInput("Plot performance graph?\n(yes/no):", ['yes', 'no'], [True, False])

    global world
    global episode
    # policy = "PRANDOM"
    # policy = "PEXPLOIT"
    # policy = "PGREEDY"

    # visualizing world in starting state
    vis_objs['world_vl'] = vl('world')
    vis_objs['world_vl'].visualize_gen(h, w)
    initWorld(h, w, world, vis_objs['world_vl'], start_x, start_y)

    vis_objs['q_table_no_block'] = vl('q_table_no_block')
    vis_objs['q_table_no_block'].visualize_gen(h, w)
    vis_objs['q_table_with_block'] = vl('q_table_with_block')
    vis_objs['q_table_with_block'].visualize_gen(h, w)

    vis_objs['agent_monitor'] = vl('agent_monitor')
    vis_objs['agent_monitor'].visualize_gen(h, w)
    initQTableWorld(h, w, world, vis_objs['agent_monitor'], start_x, start_y)

    # First drop off full
    vis_objs['first_drop_off_full'] = vl('first_drop_off_full')
    vis_objs['first_drop_off_full'].visualize_gen(h, w)
    initQTableWorld(h, w, world, vis_objs['first_drop_off_full'], start_x, start_y)
    # First terminate
    vis_objs['first_terminate'] = vl('first_terminate')
    vis_objs['first_terminate'].visualize_gen(h, w)
    initQTableWorld(h, w, world, vis_objs['first_terminate'], start_x, start_y)

    # always use PRANDOM for first 500 steps
    steps1 = doSteps(FIRST_STEPS, 'PRANDOM', method)

    # print("q_table after 500 steps")
    # print(q_table)
    if fourth_expm:
        _, _, world = ReadWorld().fill_world('testworld.txt')
        drop_off_loc = [(0, 0), (4, 0), (2, 2), (4, 4)]
        pick_up_loc = [(1, 3), (4, 2)]
        policy = "PEXPLOIT"
    # if terminal state was not reached in first 500 steps, keep going
    steps2 = 0
    if (done == False):
        steps2 = doSteps(SECOND_STEPS, policy, method)

    print("\n\nq_table after completed")
    print(q_table)

    if not done:
        episode -= 1
    print("\ncompleted", episode, 'episodes in', steps1 + steps2, "steps")
    # print('Best episode:', best_episode, 'with', best_steps, 'steps') # EXPERIMENTAL FEATURE

    # update world
    if fourth_expm:
        vis_objs['world_vl'].visualize_gen(h, w)
        initWorld(h, w, world, vis_objs['world_vl'], start_x, start_y)
    updateWorld(h, w, world, vis_objs['world_vl'])
    # update final q_table with no block
    if fourth_expm:
        vis_objs['q_table_no_block'].visualize_gen(h, w)
    fillQValues(h, w, q_table, world, vis_objs['q_table_no_block'], False, start_x, start_y)
    # update final q_table with block
    if fourth_expm:
        vis_objs['q_table_with_block'].visualize_gen(h, w)
    fillQValues(h, w, q_table, world, vis_objs['q_table_with_block'], True, start_x, start_y)
    # update agent position
    if has_block:
        putAgent(h, w, q_table, world, vis_objs['q_table_with_block'], has_block, x, y, start_x, start_y, 'ab')
    else:
        putAgent(h, w, q_table, world, vis_objs['q_table_no_block'], has_block, x, y, start_x, start_y, 'a')
    # plot
    if plot:
        plotPerformanceBank()
        plotPerformanceDelSteps()
        plt.show()

def applyAction(action):
    global drop_off_loc
    global pick_up_loc
    global has_block
    global world
    global num_of_blocks_delivered
    if action == 'd':
        world[(x, y)]['no_of_blocks'] += 1
        # DELIVER BLOCK STEPS PERFORMANCE MEASURE
        num_of_blocks_delivered += 1
        delivery_tracker[delivery_steps] = num_of_blocks_delivered

        # ----------------------------

        if world[(x, y)]['no_of_blocks'] == 4:
            drop_off_loc.remove((x, y))
            # RECORD FIRST TIME A DROP OFF IS FULL
            if episode == 1 and len(drop_off_loc) == 3:
                fillQValues(h, w, q_table, world, vis_objs['first_drop_off_full'], False, start_x, start_y)
            # -------------------------
            print((x, y), 'is full')
        has_block = False
    elif action == 'p':
        world[(x, y)]['no_of_blocks'] -= 1
        if world[(x, y)]['no_of_blocks'] == 0:
            pick_up_loc.remove((x, y))
            print((x, y), 'is empty')
        has_block = True


def bestValidAction(state, actions):
    # init max_val to first val in list
    max_val = q_table[state][actionToIndex(actions[0])]
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


def qLearning(state, action, reward, next_state, next_actions):
    return Q(state, action) + alpha * (reward + gamma * (maxQ(next_state, next_actions) - Q(state, action)))


def sarsa(state, action, reward, next_state, next_actions, policy):
    next_action = []
    if (policy == 'PRANDOM'):
        next_action, _ = chooseRandomAction(next_actions)
    elif (policy == 'PEXPLOIT'):
        next_action, _ = exploitAction(state, next_actions, epsilon)
    elif (policy == 'PGREEDY'):
        next_action, _ = greedyAction(state, next_actions)

    return Q(state, action) + alpha*(reward + gamma * (Q(next_state, next_action) - Q(state, action)))


def doSteps(steps, policy, method):
    global x, y, drop_off_loc, pick_up_loc, has_block, \
        done, world, q_offset, q_table, count_steps, episode, watch
    global num_of_blocks_delivered, delivery_steps, bank_account
    '''
    global best_q_table, best_steps, best_episode  # EXPERIMENTAL FEATURE
    '''
    step = 0
    ntw = True  # from no block to with block
    wtn = True  # from with block to no block

    for step in range(0, steps):
        delivery_steps += 1
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

        # BANK THE REWARD
        bank_account.append(bank_account[len(bank_account)-1]+reward)

        # has_block gets updated here
        applyAction(action)

        next_x, next_y = getNextCoords(action, world, x, y)
        if (coordsNotValid(next_x, next_y, w, h)): break
        next_actions = getValidActions(world, next_x, next_y, has_block)
        next_state = states[next_y][next_x]
        if (has_block): next_state += q_offset

        # update qtable
        if method == "Q_LEARNING":
            q_table[state][actionToIndex(action)] = qLearning(state, action, reward, next_state, next_actions)
        elif method == "SARSA":
            q_table[state][actionToIndex(action)] = sarsa(state, action, reward, next_state, next_actions, policy)

        # keep track of prev state for step visualize part
        prev_x = x
        prev_y = y

        # 'move' to the next state
        x = next_x
        y = next_y

        # if terminal state reached
        # reset world, put agent back at start
        if len(pick_up_loc) == 0 and len(drop_off_loc) == 0:  # or (policy == 'PGREEDY' and steps == best_steps):
            # RESET num_of_blocks_delivered
            num_of_blocks_delivered = 0
            # Put episode bank account in the bank
            regBankAccount()
            # RECORD FIRST TERMINATE
            if episode == 1:
                fillQValues(h, w, q_table, world, vis_objs['first_terminate'], False, start_x, start_y)
            # ------------------------------
            print(q_table)
            print('episode', episode, 'is done | agent takes:', count_steps, 'steps')  # ,'| best steps: ', best_steps)
            print("\nTerminal state reached")
            episode_list.append(episode)
            steps_count_list.append(count_steps)
            terminal_reached.append('True')
            done = True
            x = 0
            y = 4
            has_block = False
            done = False
            drop_off_loc = [(0, 0), (4, 0), (2, 2), (4, 4)]
            if fourth_expm and episode >= 2:
                pick_up_loc = [(0, 2), (2, 0)]
                _, _, world = ReadWorld().fill_world('testworld4thexpm.txt')
            else:
                pick_up_loc = [(1, 3), (4, 2)]
                _, _, world = ReadWorld().fill_world('testworld.txt')
            updateDropAndPickSpots(h, w, q_table, False,
                                   drop_off_loc, pick_up_loc, vis_objs['q_table_no_block'], world)
            updateDropAndPickSpots(h, w, q_table, True,
                                   drop_off_loc, pick_up_loc, vis_objs['q_table_with_block'], world)
            # reset preferable path
            vis_objs['agent_monitor'].visualize_gen(h, w)
            # print('q_table:')
            # print(q_table)
            
            # EXPERIMENTAL FEATURE
            '''
            if count_steps < best_steps :
                best_steps = count_steps
                best_q_table = q_table
                best_episode = episode
            elif count_steps >= best_steps and policy == 'PGREEDY':
                q_table = best_q_table
                print('Revert q_table')
            '''
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

        if steps != 500 and watch:
            print('\n' * 5)
            # print(q_table)
            print(valid_actions)
            print('action: {:5s}'.format(action), '| reward:', reward)
            print('ntw:', ntw, '| wtn:', wtn)
            if has_block:
                wtn = True
                if ntw:
                    fillQValues(h, w, q_table, world, vis_objs['agent_monitor'], has_block, start_x, start_y)
                    ntw = False
                updateCell(h, w, q_table, world, vis_objs['agent_monitor'],
                           has_block, prev_x, prev_y, start_x, start_y)
                putAgent(h, w, q_table, world, vis_objs['agent_monitor'], has_block, x, y, start_x, start_y, 'ab')

            else:
                ntw = True
                if wtn:
                    fillQValues(h, w, q_table, world, vis_objs['agent_monitor'], has_block, start_x, start_y)
                    wtn = False
                updateCell(h, w, q_table, world, vis_objs['agent_monitor'],
                           has_block, prev_x, prev_y, start_x, start_y)
                putAgent(h, w, q_table, world, vis_objs['agent_monitor'], has_block, x, y, start_x, start_y, 'a')

            img = cv.imread('agent_monitor.png')
            cv.imshow('agent monitor', img)
            cv.waitKey(1)

    if step + 1 == SECOND_STEPS:
        print('episode ', episode, 'is not done | agent takes:', count_steps)
        episode_list.append(episode)
        steps_count_list.append(count_steps)
        terminal_reached.append('False')        
       
        print('6000 steps reached')
    return step + 1


if __name__ == '__main__':
    main()
