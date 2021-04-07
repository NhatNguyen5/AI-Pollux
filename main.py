

def read_World(file_name):
    file = open(file_name)
    lines = file.readlines()
    file.close()
    world = []
    x = 0
    y = 0
    for line in lines:
        steps = line[:-1].split(',')
        row = []
        for step in steps:
            row.append(step)
            y += 1
        world.append(row)
        x += 1
    print(world)


def main():
    print('Hello')
    read_World('testworld.txt')

if __name__ == '__main__':
    main()

