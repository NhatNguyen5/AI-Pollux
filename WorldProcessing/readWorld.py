class ReadWorld:
    def __init__(self):
        pass

    # read world from txt file
    def read_world(self, file_name):
        file = open(file_name)
        lines = file.readlines()
        file.close()
        world = []
        x = 0
        y = 0
        for line in lines:
            line = line.replace("\n", "")
            blocks = line.split(',')
            row = []
            for block in blocks:
                row.append(block)
                y += 1
            world.append(row)
            x += 1
        return world

    # return a dictionary of blocks in that world has coor, north, south, west, east and action
    # and size of that world
    def fill_world(self, file_name):
        general_world = self.read_world(file_name)
        world = dict()
        elements = ['coor', 'north', 'south', 'west', 'east', 'action', 'no_of_block']

        no_block_h = len(general_world)
        no_block_w = len(general_world[0])

        for i in range(no_block_h):
            for j in range(no_block_w):
                world[(j, i)] = dict()
                for e in elements:
                    if e == 'coor':
                        world[(j, i)][e] = (j, i)
                    if e == 'north':
                        if i == 0:
                            world[(j, i)][e] = 'nan'
                        else:
                            world[(j, i)][e] = (j, i - 1)
                    if e == 'south':
                        if i == no_block_h:
                            world[(j, i)][e] = 'nan'
                        else:
                            world[(j, i)][e] = (j, i + 1)
                    if e == 'west':
                        if j == 0:
                            world[(j, i)][e] = 'nan'
                        else:
                            world[(j, i)][e] = (j - 1, i)
                    if e == 'east':
                        if j == no_block_w:
                            world[(j, i)][e] = 'nan'
                        else:
                            world[(j, i)][e] = (j + 1, i)
                    if e == 'action':
                        world[(j, i)][e] = general_world[i][j]
                    if()
                    if e == 'action':
                        world[(j, i)][e] = general_world[i][j]

        return no_block_h, no_block_w, world
