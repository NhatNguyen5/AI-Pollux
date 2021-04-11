    
def initWorld(h, w, world, world_vl, x, y):
    for r in range(h):
        for c in range(w):
            if world[(c, r)]['action'] == 'd': world_vl.fill_block(world[(c, r)]['coor'], 'green')
            if world[(c, r)]['action'] == 'p': world_vl.fill_block(world[(c, r)]['coor'], 'blue')
            world_vl.write_block(world[(c, r)]['coor'], world[(c, r)]['action'], 'white')
            world_vl.write_block(world[(c, r)]['coor'], str(world[(c, r)]['coor']), 'black', 'n', 15)
    world_vl.fill_block(world[(x, y)]['coor'], 'yellow')
    world_vl.write_block(world[(x, y)]['coor'], 'start', 'black')

def updateWorld(h, w, world, world_vl):
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