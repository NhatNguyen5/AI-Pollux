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
        elements = ['coor', 'north', 'south', 'west', 'east', 'action', 'no_of_blocks', 'step_scores', 'direction']

        num_cells_h = len(general_world)
        num_cells_w = len(general_world[0])

        for i in range(num_cells_w):
            for j in range(num_cells_h):
                world[(i, j)] = dict()
                for e in elements:
                    if e == 'coor':
                        world[(i, j)][e] = (i, j)
                    if e == 'north':
                        if j == 0:
                            world[(i, j)][e] = 'nan'
                        else:
                            world[(i, j)][e] = (i, j - 1)
                    if e == 'south':
                        if j == num_cells_h - 1:
                            world[(i, j)][e] = 'nan'
                        else:
                            world[(i, j)][e] = (i, j + 1)
                    if e == 'west':
                        if i == 0:
                            world[(i, j)][e] = 'nan'
                        else:
                            world[(i, j)][e] = (i - 1, j)
                    if e == 'east':
                        if i == num_cells_w-1:
                            world[(i, j)][e] = 'nan'
                        else:
                            world[(i, j)][e] = (i + 1, j)
                    if e == 'action':
                        world[(i, j)][e] = general_world[j][i]
                    if e == 'no_of_blocks':
                        if general_world[j][i] == 'p':
                            world[(i, j)][e] = 8
                        else:
                            world[(i, j)][e] = 0
                    if e == 'step_scores':
                        world[(i, j)][e] = 0
                    if e == 'direction':
                        world[(i, j)][e] = ''
        return num_cells_h, num_cells_w, world
