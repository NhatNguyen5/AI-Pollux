# AI-Pollux

AI group project.

global world:
world has blocks, which has 'coor'(it's coordinate), 'north', 'south', 'west', 'east'
it's neighbor blocks(edges and corner will have some nan neighbors)
and action(0 is nothing, 'd' is drop and 'p' is pick up,
block and it's elements can be access with world[(x, y)]['key']

Visualization:
read_world(file_name) // read world from file
fill_world(file_name) // fill a world dictionary
visualize_gen(no_block_h, no_block_w, world) // Generate a picture
fill_block((x, y), 'color') // fill block at x, y with color
write_block((x, y), txt, 'color', 'pos') // write a color txt to block at x, y, pos in the block (n, s, w, e, c)
put_x((x, y), 'color') // put a big X on the block
