from functions import *


def initWorld(h, w, world, world_vl, x, y):
    for r in range(h):
        for c in range(w):
            if world[(c, r)]['action'] == 'd': world_vl.fill_block(world[(c, r)]['coor'], 'forestgreen')
            if world[(c, r)]['action'] == 'p': world_vl.fill_block(world[(c, r)]['coor'], 'dodgerblue')
            if(r == y and c == x):
                world_vl.fill_block(world[(x, y)]['coor'], 'gold')
                world_vl.write_block(world[(x, y)]['coor'], 'start', 'indigo')
            else:
                world_vl.write_block(world[(c, r)]['coor'], world[(c, r)]['action'], 'white')
            world_vl.write_block(world[(c, r)]['coor'], str(world[(c, r)]['coor']), 'black', 'n', 15)
    print('Done init world')

def updateWorld(h, w, world, world_vl, x, y):
    for r in range(h):
        for c in range(w):
            ss = world[(c, r)]['step_scores']
            world_vl.fill_block(world[(c, r)]['coor'], (3*ss + 128, 2*ss + 128, ss + 128))
            if world[(c, r)]['action'] == 'd': world_vl.fill_block(world[(c, r)]['coor'], 'forestgreen')
            if world[(c, r)]['action'] == 'p': world_vl.fill_block(world[(c, r)]['coor'], 'dodgerblue')
            if(r == y and c == x):
                world_vl.fill_block(world[(x, y)]['coor'], 'gold')
                world_vl.write_block(world[(x, y)]['coor'], 'start', 'indigo')
            else:
                world_vl.write_block(world[(c, r)]['coor'], world[(c, r)]['action'], 'white')
            world_vl.write_block(world[(c, r)]['coor'], str(world[(c, r)]['coor']), 'black', 'n', 15)
            if world[(c, r)]['action'] == 'd' or world[(c, r)]['action'] == 'p':
                world_vl.write_block(world[(c, r)]['coor'], str(world[(c, r)]['no_of_blocks']), 'black', pos='s')
    print('Done update world')

def initQTableWorld(h, w, world, world_vl, x, y):
    for r in range(h):
        for c in range(w):
            if world[(c, r)]['action'] == 'd': world_vl.fill_block(world[(c, r)]['coor'], 'forestgreen')
            if world[(c, r)]['action'] == 'p': world_vl.fill_block(world[(c, r)]['coor'], 'dodgerblue')
            if (r == y and c == x):
                world_vl.fill_block(world[(x, y)]['coor'], 'gold')
                world_vl.put_x((c, r), 'purple')
                world_vl.write_block(world[(x, y)]['coor'], 'start', 'indigo', font_s=12)
            else:
                world_vl.fill_block(world[(x, y)]['coor'], world_vl.get_color(x, y))
                world_vl.put_x((c, r), 'purple')
                world_vl.write_block(world[(c, r)]['coor'], world[(c, r)]['action'], 'white')
            world_vl.write_block(world[(c, r)]['coor'], str(world[(c, r)]['coor']), 'black', 'n', 9, offset_u=8)
    print('Done init Q table')

def fillQValues(h, w, q_table, world, world_vl, has_block, start_x, start_y):
    for r in range(w):
        for c in range(h):
            updateCell(h, w, q_table, world, world_vl, has_block, r, c, start_x, start_y, True)
    print('Done filling Q values')

def putAgent(h, w, q_table, world, world_vl, has_block, x, y, start_x, start_y, agent_name='a'):
    updateCell(h, w, q_table, world, world_vl, has_block, x, y, start_x, start_y)
    world_vl.write_block(world[(x, y)]['coor'], str(agent_name), 'red', font_s=20)

def updateCell(h, w, q_table, world, world_vl, has_block, prev_x, prev_y, start_x, start_y, is_fillQ=False):
    # actions = ['n', 's', 'e', 'w']
    actions = []
    q_offset = 0
    ss = world[(prev_x, prev_y)]['step_scores']
    if is_fillQ:
        # world_vl.fill_block(world[(prev_x, prev_y)]['coor'], world_vl.get_color(prev_x, prev_y))
        world_vl.fill_block(world[(prev_x, prev_y)]['coor'], (3*ss + 128, 2*ss + 128, ss + 128))
    else:
        world_vl.fill_block(world[(prev_x, prev_y)]['coor'], pathen(prev_x, prev_y, world_vl))
    if world[(prev_x, prev_y)]['action'] == 'd': world_vl.fill_block(world[(prev_x, prev_y)]['coor'], 'forestgreen')
    if world[(prev_x, prev_y)]['action'] == 'p': world_vl.fill_block(world[(prev_x, prev_y)]['coor'], 'dodgerblue')
    if (prev_y == start_y and prev_x == start_x):
        world_vl.fill_block(world[(prev_x, prev_y)]['coor'], 'gold')
        world_vl.put_x((prev_x, prev_y), 'purple')
        world_vl.write_block(world[(prev_x, prev_y)]['coor'], 'start', 'indigo', font_s=12)
    else:
        world_vl.put_x((prev_x, prev_y), 'purple')
        world_vl.write_block(world[(prev_x, prev_y)]['coor'], world[(prev_x, prev_y)]['action'], 'white')
        world_vl.write_block(world[(prev_x, prev_y)]['coor'],
                             str(world[(prev_x, prev_y)]['coor']), 'black', 'n', 9, offset_u=8)
    if world[(prev_x, prev_y)]['action'] == 'd' or world[(prev_x, prev_y)]['action'] == 'p':
        world_vl.write_block(world[(prev_x, prev_y)]['coor'],
                             str(world[(prev_x, prev_y)]['no_of_blocks']), 'black', pos='s', font_s=9, offset_u=10)
    if (has_block == True):
        q_offset = w * h
    state = getStateFromCoords(prev_y, prev_x) + q_offset
    valid_actions = getValidActions(world, prev_x, prev_y, has_block)
    if valid_actions[0] == 'd' or valid_actions[0] == 'p':
        valid_actions = getValidActions(world, prev_x, prev_y, not has_block)
    check_max_list = []
    for va in valid_actions:
        i = actionToIndex(va)
        if va == 'north':
            check_max_list.append(q_table[state][i])
            actions.append('n')
        elif va == 'south':
            check_max_list.append(q_table[state][i])
            actions.append('s')
        elif va == 'east':
            check_max_list.append(q_table[state][i])
            actions.append('e')
        elif va == 'west':
            check_max_list.append(q_table[state][i])
            actions.append('w')
    for va, a in zip(valid_actions, actions):
        i = actionToIndex(va)
        max_q_value = max(check_max_list)
        if q_table[state][i] != max_q_value:
            world_vl.write_block((prev_x, prev_y), str(round(q_table[state][i], 2)), 'black',
                                 pos=a, font_s=10)
        else:
            world_vl.write_block((prev_x, prev_y), str(round(q_table[state][i], 2)), 'maroon',
                                 pos=a, font_s=10)


def updateDropAndPickSpots(h, w, q_table, has_block, drop_off_loc, pick_up_loc, world_vl, world):
    loc_list = drop_off_loc + pick_up_loc
    actions = []
    q_offset = 0
    for c in loc_list:
        if world[c]['action'] == 'd': world_vl.fill_block(world[c]['coor'], 'forestgreen')
        if world[c]['action'] == 'p': world_vl.fill_block(world[c]['coor'], 'dodgerblue')
        world_vl.put_x(c, 'purple')
        world_vl.write_block(world[c]['coor'], world[c]['action'], 'white')
        world_vl.write_block(world[c]['coor'],
                             str(world[c]['coor']), 'black', 'n', 9, offset_u=8)
        world_vl.write_block(world[c]['coor'], str(world[c]['no_of_blocks']), 'black',
                             pos='s', font_s=9, offset_u=10)
        if (has_block == True):
            q_offset = w * h
        state = getStateFromCoords(c[1], c[0]) + q_offset
        valid_actions = getValidActions(world, c[0], c[1], has_block)
        if valid_actions[0] == 'd' or valid_actions[0] == 'p':
            valid_actions = getValidActions(world, c[0], c[1], not has_block)
        check_max_list = []
        for va in valid_actions:
            i = actionToIndex(va)
            if va == 'north':
                check_max_list.append(q_table[state][i])
                actions.append('n')
            elif va == 'south':
                check_max_list.append(q_table[state][i])
                actions.append('s')
            elif va == 'east':
                check_max_list.append(q_table[state][i])
                actions.append('e')
            elif va == 'west':
                check_max_list.append(q_table[state][i])
                actions.append('w')
        for va, a in zip(valid_actions, actions):
            i = actionToIndex(va)
            max_q_value = max(check_max_list)
            if q_table[state][i] != max_q_value:
                world_vl.write_block(c, str(round(q_table[state][i], 2)), 'black',
                                     pos=a, font_s=10)
            else:
                world_vl.write_block(c, str(round(q_table[state][i], 2)), 'maroon',
                                     pos=a, font_s=10)


def pathen(x, y, world_vl):
    r, g, b = world_vl.get_color(x, y)
    return r + 3, g + 2, b
