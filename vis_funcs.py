from functions import *


def initWorld(h, w, world, world_vl, x, y):

    for r in range(h):
        for c in range(w):
            if world[(c, r)]['action'] == 'd': world_vl.fill_block(world[(c, r)]['coor'], 'green')
            if world[(c, r)]['action'] == 'p': world_vl.fill_block(world[(c, r)]['coor'], 'blue')
            if(r == y and c == x):
                world_vl.fill_block(world[(x, y)]['coor'], 'yellow')
                world_vl.write_block(world[(x, y)]['coor'], 'start', 'black')
            else:
                world_vl.write_block(world[(c, r)]['coor'], world[(c, r)]['action'], 'white')
            world_vl.write_block(world[(c, r)]['coor'], str(world[(c, r)]['coor']), 'black', 'n', 15)
    print('Done initializing visual')

def updateWorld(h, w, world, world_vl):
    for r in range(h):
        for c in range(w):
            if world[(c, r)]['action'] == 'd' or world[(c, r)]['action'] == 'p':
                world_vl.write_block(world[(c, r)]['coor'], str(world[(c, r)]['no_of_blocks']), 'black', pos='s')
    print('Done updating visual')

def initQTableWorld(h, w, world, world_vl, x, y):
    for r in range(h):
        for c in range(w):
            if world[(c, r)]['action'] == 'd': world_vl.fill_block(world[(c, r)]['coor'], 'green')
            if world[(c, r)]['action'] == 'p': world_vl.fill_block(world[(c, r)]['coor'], 'blue')
            if (r == y and c == x):
                world_vl.fill_block(world[(x, y)]['coor'], 'yellow')
                world_vl.put_x((c, r), 'purple')
                world_vl.write_block(world[(x, y)]['coor'], 'start', 'black')
            else:
                world_vl.put_x((c, r), 'purple')
                world_vl.write_block(world[(c, r)]['coor'], world[(c, r)]['action'], 'white')
            world_vl.write_block(world[(c, r)]['coor'], str(world[(c, r)]['coor']), 'black', 'n', 9, offset_u=10)
    print('Done initializing q_table')

def updateQTableWorld(h, w, world, world_vl, x, y):
    for r in range(h):
        for c in range(w):
            if world[(c, r)]['action'] == 'd' or world[(c, r)]['action'] == 'p':
                world_vl.write_block(world[(c, r)]['coor'], str(world[(c, r)]['no_of_blocks']), 'black',
                                     pos='s', font_s=9, offset_u=10)
    print('Done updating q_table')

def fillQValues(h, w, q_table, world_vl, has_block):
    action = ['n', 's', 'e', 'w']
    q_offset = 0
    if(has_block == True):
        q_offset = w * h
    for r in range(w):
        for c in range(h):
            state = getStateFromCoords(c, r) + q_offset
            for i, a in enumerate(action):
                world_vl.write_block((r, c), str(q_table[state][i]), 'black',
                                     pos=a, font_s=10)
    print('Done filling q_table')

def putAgent(h, w, q_table, world, world_vl, has_block, x, y, start_x, start_y):
    updateCell(h, w, q_table, world, world_vl, has_block, x, y, start_x, start_y)
    world_vl.write_block(world[(x, y)]['coor'], 'a', 'red')

def updateCell(h, w, q_table, world, world_vl, has_block, prev_x, prev_y, start_x, start_y):
    action = ['n', 's', 'e', 'w']
    q_offset = 0
    world_vl.fill_block(world[(prev_x, prev_y)]['coor'], 'gray')
    if world[(prev_x, prev_y)]['action'] == 'd': world_vl.fill_block(world[(prev_x, prev_y)]['coor'], 'green')
    if world[(prev_x, prev_y)]['action'] == 'p': world_vl.fill_block(world[(prev_x, prev_y)]['coor'], 'blue')
    if (prev_y == start_y and prev_x == start_x):
        world_vl.fill_block(world[(prev_x, prev_y)]['coor'], 'yellow')
        world_vl.put_x((prev_x, prev_y), 'purple')
        world_vl.write_block(world[(prev_x, prev_y)]['coor'], 'start', 'black')
    else:
        world_vl.put_x((prev_x, prev_y), 'purple')
        world_vl.write_block(world[(prev_x, prev_y)]['coor'], world[(prev_x, prev_y)]['action'], 'white')
        world_vl.write_block(world[(prev_x, prev_y)]['coor'],
                             str(world[(prev_x, prev_y)]['coor']), 'black', 'n', 9, offset_u=10)
    if world[(prev_x, prev_y)]['action'] == 'd' or world[(prev_x, prev_y)]['action'] == 'p':
        world_vl.write_block(world[(prev_x, prev_y)]['coor'],
                             str(world[(prev_x, prev_y)]['no_of_blocks']), 'black', pos='s', font_s=9, offset_u=10)
    if (has_block == True):
        q_offset = w * h
    state = getStateFromCoords(prev_y, prev_x) + q_offset
    for i, a in enumerate(action):
        world_vl.write_block((prev_x, prev_y), str(q_table[state][i]), 'black',
                             pos=a, font_s=10)


def updateDropAndPickSpots(h, w, q_table, has_block, drop_off_loc, pick_up_loc, world_vl, world):
    loc_list = drop_off_loc + pick_up_loc
    action = ['n', 's', 'e', 'w']
    q_offset = 0
    for c in loc_list:
        if world[c]['action'] == 'd': world_vl.fill_block(world[c]['coor'], 'green')
        if world[c]['action'] == 'p': world_vl.fill_block(world[c]['coor'], 'blue')
        world_vl.put_x(c, 'purple')
        world_vl.write_block(world[c]['coor'], world[c]['action'], 'white')
        world_vl.write_block(world[c]['coor'],
                             str(world[c]['coor']), 'black', 'n', 9, offset_u=10)
        world_vl.write_block(world[c]['coor'], str(world[c]['no_of_blocks']), 'black',
                             pos='s', font_s=9, offset_u=10)
        if (has_block == True):
            q_offset = w * h
        state = getStateFromCoords(c[1], c[0]) + q_offset
        for i, a in enumerate(action):
            world_vl.write_block(c, str(q_table[state][i]), 'black',
                                 pos=a, font_s=10)

