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


def updateWorld(h, w, world, world_vl):
    for r in range(h):
        for c in range(w):
            if world[(c, r)]['action'] == 'd' or world[(c, r)]['action'] == 'p':
                world_vl.write_block(world[(c, r)]['coor'], str(world[(c, r)]['no_of_blocks']), 'black', pos='s')


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

def updateQTableWorld(h, w, world, world_vl):
    for r in range(h):
        for c in range(w):
            if world[(c, r)]['action'] == 'd' or world[(c, r)]['action'] == 'p':
                world_vl.write_block(world[(c, r)]['coor'], str(world[(c, r)]['no_of_blocks']), 'black',
                                     pos='s', font_s=10, offset_u=14)


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



