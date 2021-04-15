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

alpha = 0.3  # learning rate
gamma = 0.5  # discount rate
epsilon = 0.8  # chance of being greedy in exploit policy

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

# BANK ACCOUNT (USE FOR MEASURING PERFORMANCE)
bank_plot_steps = np.arange(SECOND_STEPS)  # step array use for plotting
bank = []
bank_account = [0]

# DELIVERY STEPS (MEASURE PERFORMANCE)
delivery_plot_steps = np.arange(FIRST_STEPS + SECOND_STEPS)
delivery_steps = 0
prev_del_step = 0
num_of_blocks_delivered = 0
delivery_tracker = np.zeros(FIRST_STEPS + SECOND_STEPS)

# 4th experiment enabler
fourth_expm = False

# visualize each step
watch = False

# Ask for continue after each episode
pit_stop = False


def regBankAccount():
    global bank_account
    bank.append(bank_account)
    bank_account = [0]


def plotPerformanceBank(name='performance_bank_plot'):
    plt.figure(1)
    max_len = []
    for ba in bank:
        max_len.append(len(ba))
    for i, ba in enumerate(bank):
        plt.plot(bank_plot_steps[:max(max_len)],
                 np.pad(ba, (0, max(max_len) - len(ba)),
                        'constant', constant_values=ba[len(ba) - 1]), label='E%d' % (i + 1))
    plt.title('Reward performance graph')
    plt.xlabel('Steps')
    plt.ylabel('Accumulated reward')
    plt.legend()
    plt.savefig('Images/%s.png' % name)
    plt.clf()


def plotPerformanceDelSteps(name='performance_del_steps_plot'):
    plt.figure(2)
    curr_nob = -1
    last_pos = -1
    track = -1
    snapshot_delivery_tracker = delivery_tracker[:delivery_steps]
    snapshot_delivery_plot_steps = delivery_plot_steps[:delivery_steps]
    while snapshot_delivery_tracker[track] != num_of_blocks_delivered: track -= 1
    for j in range(delivery_steps + track, delivery_steps):
        snapshot_delivery_tracker[j] = num_of_blocks_delivered
    for i, n in enumerate(snapshot_delivery_tracker):
        if curr_nob == 15:
            curr_nob = -1
        if n == curr_nob + 1:
            curr_nob += 1
            incre = 1/(i - last_pos)
            for j in range(last_pos + 1, i):
                snapshot_delivery_tracker[j] = snapshot_delivery_tracker[j-1] + incre
            last_pos = i
    plt.plot(snapshot_delivery_plot_steps, snapshot_delivery_tracker)
    plt.title('Blocks delivered performance graph')
    plt.xlabel('Steps')
    plt.ylabel('Block delivered')
    plt.savefig('Images/%s.png' % name)


def output_to_exel(df_marks):
    writer = pd.ExcelWriter('output' + '.xlsx')
    # write dataframe to excel
    df_marks.to_excel(writer)
    # save the excel
    writer.save()
    print('DataFrame is written successfully to Excel File.')


def getAcceptedInput(question, accepted_inputs, return_values):
    user_input = input(question)
    while not (user_input in accepted_inputs):
        print('Input not valid, try again!')
        user_input = input(question)
    else:
        return return_values[accepted_inputs.index(user_input)]


def getFloat(name):
    while True:
        val = float(input("\nEnter value for " + name + ": "))
        if val < 1 and val > 0:
            break
        print('\nInvalid input! \n', name, 'must be between 0 and 1')
    return val

def main():
    global fourth_expm, watch, pit_stop, drop_off_loc, pick_up_loc, alpha, gamma, epsilon, episode, world
    default = getAcceptedInput("Use default (Q_LEARNING, PEXPLOIT, no monitor, plot, no asking for continue)?"
                               "\n(yes/no): ", ['yes', 'no'], [True, False])
    policy = ''
    if default:
        method = "Q_LEARNING"
        policy = "PEXPLOIT"
        watch = False
        plot = True
        pit_stop = False
    else:
        method = getAcceptedInput("Which learning method?\n(Q_LEARNING/SARSA): ",
                                  ["Q_LEARNING", "SARSA"], ["Q_LEARNING", "SARSA"])
        fourth_expm = getAcceptedInput("Enable fourth experiment?\n(yes/no): ", ['yes', 'no'], [True, False])
        if not fourth_expm:
            policy = getAcceptedInput("Which policy?\n(PRANDOM/PEXPLOIT/PGREEDY): ",
                                      ["PRANDOM", "PEXPLOIT", "PGREEDY"], ["PRANDOM", "PEXPLOIT", "PGREEDY"])
            if not getAcceptedInput("Use default parameters (alpha = 0.3, gamma = 0.5, epsilon = 0.8)?"
                                    "\n(yes/no): ", ['yes', 'no'], [True, False]):
                alpha = getFloat('alpha')
                gamma = getFloat('gamma')
                epsilon = getFloat('epsilon')
                
        watch = getAcceptedInput("Monitor agent?\n(yes/no): ", ['yes', 'no'], [True, False])
        pit_stop = getAcceptedInput("Ask for continue after each terminate?\n(yes/no): ", ['yes', 'no'], [True, False])
        plot = getAcceptedInput("Plot performance graph?\n(yes/no): ", ['yes', 'no'], [True, False])


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

    if fourth_expm:
        _, _, world = ReadWorld().fill_world('testworld.txt')
        drop_off_loc = [(0, 0), (4, 0), (2, 2), (4, 4)]
        pick_up_loc = [(1, 3), (4, 2)]
        policy = "PEXPLOIT"
    # if terminal state was not reached in first 500 steps, keep going
    steps2 = 0
    if (done == False):
        steps2 = doSteps(SECOND_STEPS, policy, method)

    if not done:
        episode -= 1
    print("\ncompleted", episode, 'episodes in', steps1 + steps2, "steps")

    # update world
    if fourth_expm:
        vis_objs['world_vl'].visualize_gen(h, w)
        initWorld(h, w, world, vis_objs['world_vl'], start_x, start_y)
    updateWorld(h, w, world, vis_objs['world_vl'], start_x, start_y)
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

def applyAction(action, state):
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
        if world[(x, y)]['no_of_blocks'] == 4:
            drop_off_loc.remove((x, y))
            # RECORD FIRST TIME A DROP OFF IS FULL
            if episode == 1 and len(drop_off_loc) == 3:
                fillQValues(h, w, q_table, world, vis_objs['first_drop_off_full'], False, start_x, start_y)
        has_block = False
    elif action == 'p':
        world[(x, y)]['no_of_blocks'] -= 1
        if world[(x, y)]['no_of_blocks'] == 0:
            pick_up_loc.remove((x, y))
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
    step = 0
    ntw = True  # from no block to with block
    wtn = True  # from with block to no block

    for step in range(0, steps):
        state = states[y][x]
        if (has_block): state += q_offset
        world[(x, y)]['step_scores'] += 1
        action = ''
        reward = -1

        valid_actions = getValidActions(world, x, y, has_block)
        if (policy == 'PRANDOM'):
            action, reward = chooseRandomAction(valid_actions)
        elif (policy == 'PEXPLOIT'):
            action, reward = exploitAction(state, valid_actions, epsilon)
        elif (policy == 'PGREEDY'):
            action, reward = greedyAction(state, valid_actions)
        bank_account.append(bank_account[len(bank_account)-1]+reward)

        # has_block gets updated here
        applyAction(action, state)
        # Register a step between delivery
        delivery_steps += 1

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

        # RESET Q_VALUES FOR DELI AND PICK SPOT WHEN FULL AND EMPTY
        '''
        if action == 'd':
            if world[(x, y)]['no_of_blocks'] == 4:
                q_table[state][5] = 0
        elif action == 'p':
            if world[(x, y)]['no_of_blocks'] == 0:
                q_table[state][4] = 0
        '''
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

            print("Terminal state reached")
            print('episode', episode, 'is done | agent took', count_steps, 'steps')  # ,'| best steps: ', best_steps)
            episode_list.append(episode)
            steps_count_list.append(count_steps)
            terminal_reached.append('True')

            # reset episode steps
            count_steps = 0
            done = True
            x = 0
            y = 4
            has_block = False
            done = False
            drop_off_loc = [(0, 0), (4, 0), (2, 2), (4, 4)]
            if watch:
                if getAcceptedInput("Take a snapshot?\n(yes/no): ", ['yes', 'no'], [True, False]):
                    vis_objs['agent_monitor'].snapshot(input("Save as: "))
                if not getAcceptedInput("Continue?\n(yes/no): ", ['yes', 'no'], [True, False]):
                    episode += 1
                    break
            if pit_stop:
                if getAcceptedInput("Take a snapshot?\n(yes/no): ", ['yes', 'no'], [True, False]):
                    updateWorld(h, w, world, vis_objs['world_vl'], start_x, start_y)
                    fillQValues(h, w, q_table, world, vis_objs['q_table_no_block'], False, start_x, start_y)
                    fillQValues(h, w, q_table, world, vis_objs['q_table_with_block'], True, start_x, start_y)
                    if has_block:
                        putAgent(h, w, q_table, world, vis_objs['q_table_with_block'],
                                 has_block, x, y, start_x, start_y, 'ab')
                    else:
                        putAgent(h, w, q_table, world, vis_objs['q_table_no_block'],
                                 has_block, x, y, start_x, start_y, 'a')
                    vis_objs['q_table_with_block'].snapshot('E%d_q_table_with_block' % episode)
                    vis_objs['q_table_no_block'].snapshot('E%d_q_table_no_block' % episode)
                    vis_objs['world_vl'].snapshot('E%d_world' % episode)
                    plotPerformanceBank('E%d_performance_bank_plot' % episode)
                    plotPerformanceDelSteps('E%d_performance_del_steps_plot' % episode)
                if not getAcceptedInput("Continue?\n(yes/no): ", ['yes', 'no'], [True, False]):
                    episode += 1
                    break
                watch = getAcceptedInput("Monitor agent?\n(yes/no): ", ['yes', 'no'], [True, False])

            if fourth_expm and episode >= 2:
                pick_up_loc = [(0, 2), (2, 0)]
                _, _, world = ReadWorld().fill_world('testworld4thexpm.txt')
            else:
                pick_up_loc = [(1, 3), (4, 2)]
                _, _, world = ReadWorld().fill_world('testworld.txt')
            # count episode
            episode += 1
            updateDropAndPickSpots(h, w, q_table, False, drop_off_loc, pick_up_loc, vis_objs['q_table_no_block'], world)
            updateDropAndPickSpots(h, w, q_table, True, drop_off_loc, pick_up_loc, vis_objs['q_table_with_block'], world)
            # reset preferable path
            vis_objs['agent_monitor'].visualize_gen(h, w)
            
            print('\n-------------------------------------------------\n')
            # break

        # break if the next x or y is not valid (should never happen)
        if (coordsNotValid(x, y, w, h)): break

        # count episode steps
        count_steps += 1

        # AGENT MONITOR
        if watch and steps != 500:
            print('\n' * 5)
            print(valid_actions)
            print(q_table[state])
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

            img = cv.imread('Images/agent_monitor.png')
            cv.imshow('agent monitor', img)
            cv.waitKey(0)

    # output for the last episode
    if step + 1 == SECOND_STEPS:
        print('episode ', episode, 'is not done | agent took:', count_steps, 'steps')
        episode_list.append(episode)
        steps_count_list.append(count_steps)
        terminal_reached.append('False')  
        df_marks = pd.DataFrame({'episodes': episode_list,
                             'steps counted': steps_count_list,
                             'Terminal state reached': terminal_reached,
                             })
        output_to_exel(df_marks)

    return step + 1


if __name__ == '__main__':
    main()
