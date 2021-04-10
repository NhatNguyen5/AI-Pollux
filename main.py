import numpy as np

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


def getApplicableOperators(world, x, y, hasBlock, blocksIn11, blocksIn15, blocksin33, blocksIn35, blocksIn33, blocksIn42, blocksIn55):
    
    directions = ['north', 'south', 'west', 'east']
    return_dir = []

    if (hasBlock):
        if (world[(x, y)]['action'] == "d" and world[(x,y)]['no_of_block'] < 4):
            return "d"
        for d in directions:
            if world[(x, y)][d] != 'nan':
                return_dir.append(world[(x, y)][d]
        

def main():
    print('Hello')
    h, w, world = ReadWorld().fill_world('testworld.txt')
    # print(world)
    world_vl = vl()

    world_vl.visualize_gen(h, w, world)
    # fill_block((0, 0), 'green')
    # write_block((0, 0), 'Hello', 'white', 'n')
    # put_x((0, 0), 'white')


    for r in range(w):
        for c in range(h):
            if world[(c, r)]['action'] == 'd':
                world_vl.fill_block(world[(c, r)]['coor'], 'green')
            if world[(c, r)]['action'] == 'p':
                world_vl.fill_block(world[(c, r)]['coor'], 'blue')
            world_vl.write_block(world[(c, r)]['coor'], world[(c, r)]['action'], 'white')


    initial_state = (0, 0)

    print(world[0, 1]['action'])
    q_table = np.zeros((w, h, 6))
    print(q_table)
    action = ['n', 's', 'w', 'e', 'p', 'd']


    #  start episode

    FIRST_STEPS = 500
    SECOND_STEPS = 5500
    policy = "PRANDOM"
    # policy = "PEXPLOIT"
    # policy = "PGREEDY"

    current_state = initial_state

# always use PRANDOM for first 500 steps
    for _ in range(0, FIRST_STEPS):
        applicable_operators = getApplicableOperators(world, x, y)

# chose policy for next 5500 steps
    # for _ in range(0, SECOND_STEPS):

    
    # action = np.argmax(q_table[state, :])
    for e in world[(0, 0)]:
        print(world[(0, 0)][e])

    


if __name__ == '__main__':
    main()

