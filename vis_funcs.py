from functions import *


def initWorld(h, w, world, world_vl, x, y):

    for r in range(h):
        for c in range(w):
            if world[(c, r)]['action'] == 'd': world_vl.fill_block(world[(c, r)]['coor'], 'forestgreen')
            if world[(c, r)]['action'] == 'p': world_vl.fill_block(world[(c, r)]['coor'], 'dodgerblue')
            if(r == y and c == x):
                world_vl.fill_block(world[(x, y)]['coor'], 'gold')
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
            if world[(c, r)]['action'] == 'd': world_vl.fill_block(world[(c, r)]['coor'], 'forestgreen')
            if world[(c, r)]['action'] == 'p': world_vl.fill_block(world[(c, r)]['coor'], 'dodgerblue')
            if (r == y and c == x):
                world_vl.fill_block(world[(x, y)]['coor'], 'gold')
                world_vl.put_x((c, r), 'purple')
                world_vl.write_block(world[(x, y)]['coor'], 'start', 'black', font_s=12)
            else:
                world_vl.fill_block(world[(x, y)]['coor'], world_vl.get_color(x, y))
                world_vl.put_x((c, r), 'purple')
                world_vl.write_block(world[(c, r)]['coor'], world[(c, r)]['action'], 'white')
            world_vl.write_block(world[(c, r)]['coor'], str(world[(c, r)]['coor']), 'black', 'n', 9, offset_u=10)
    print('Done initializing q_table')

def fillQValues(h, w, q_table, world, world_vl, has_block, start_x, start_y):
    for r in range(w):
        for c in range(h):
            updateCell(h, w, q_table, world, world_vl, has_block, r, c, start_x, start_y, True)
    print('Done filling q_table')

def putAgent(h, w, q_table, world, world_vl, has_block, x, y, start_x, start_y, agent_name='a'):
    updateCell(h, w, q_table, world, world_vl, has_block, x, y, start_x, start_y)
    world_vl.write_block(world[(x, y)]['coor'], str(agent_name), 'red')

def updateCell(h, w, q_table, world, world_vl, has_block, prev_x, prev_y, start_x, start_y, is_fillQ=False):
    action = ['n', 's', 'e', 'w']
    q_offset = 0
    if is_fillQ:
        world_vl.fill_block(world[(prev_x, prev_y)]['coor'], world_vl.get_color(prev_x, prev_y))
    else:
        world_vl.fill_block(world[(prev_x, prev_y)]['coor'], pathen(prev_x, prev_y, world_vl))
    if world[(prev_x, prev_y)]['action'] == 'd': world_vl.fill_block(world[(prev_x, prev_y)]['coor'], 'forestgreen')
    if world[(prev_x, prev_y)]['action'] == 'p': world_vl.fill_block(world[(prev_x, prev_y)]['coor'], 'dodgerblue')
    if (prev_y == start_y and prev_x == start_x):
        world_vl.fill_block(world[(prev_x, prev_y)]['coor'], 'gold')
        world_vl.put_x((prev_x, prev_y), 'purple')
        world_vl.write_block(world[(prev_x, prev_y)]['coor'], 'start', 'black', font_s=12)
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
        world_vl.write_block((prev_x, prev_y), str(round(q_table[state][i], 2)), 'black',
                             pos=a, font_s=10)


def updateDropAndPickSpots(h, w, q_table, has_block, drop_off_loc, pick_up_loc, world_vl, world):
    loc_list = drop_off_loc + pick_up_loc
    action = ['n', 's', 'e', 'w']
    q_offset = 0
    for c in loc_list:
        if world[c]['action'] == 'd': world_vl.fill_block(world[c]['coor'], 'forestgreen')
        if world[c]['action'] == 'p': world_vl.fill_block(world[c]['coor'], 'dodgerblue')
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
            world_vl.write_block(c, str(round(q_table[state][i], 2)), 'black',
                                 pos=a, font_s=10)


def pathen(x, y, world_vl):
    r, g, b = world_vl.get_color(x, y)
    return r + 4, g + 2, b
