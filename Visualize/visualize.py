from PIL import Image, ImageDraw, ImageFont, ImageOps

gap = 12
block_size = 100
font_size = 20


class Visualize:
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
        elements = ['coor', 'north', 'south', 'west', 'east', 'action']

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
        return no_block_h, no_block_w, world

    # generate world image
    def visualize_gen(self, no_block_h, no_block_w, world):
        img_h = no_block_h * (block_size + gap) + gap
        img_w = no_block_w * (block_size + gap) + gap

        img = Image.new('RGB', (img_w, img_h), color='gray')
        draw = ImageDraw.Draw(img)

        # row divider
        for r in range(no_block_h + 1):
            start_p_r = (block_size + gap) * r + gap / 2
            draw.line([(0, start_p_r), (img_w, start_p_r)], fill=0, width=gap + 1)
        # col divider
        for r in range(no_block_w + 1):
            start_p_c = (block_size + gap) * r + gap / 2
            draw.line([(start_p_c, 0), (start_p_c, img_h)], fill=0, width=gap + 1)

        img.save('world.png')
        print('Done initialize visual')

    def fill_block(self, coor=(0, 0), color='white'):
        x = coor[0]
        y = coor[1]
        start_pixel_x = gap + x * (block_size + gap)
        start_pixel_y = gap + y * (block_size + gap)
        with Image.open("world.png") as img:
            draw = ImageDraw.Draw(img)
            draw.rectangle((start_pixel_x + 1, start_pixel_y + 1,
                            start_pixel_x + block_size - 0.5, start_pixel_y + block_size - 0.5),
                           fill=color)
            img.save('world.png')

    def write_block(self, coor=(0, 0), txt='text', t_color='white', pos='c'):
        x = coor[0]
        y = coor[1]
        start_pixel_x = gap + x * (block_size + gap)
        start_pixel_y = gap + y * (block_size + gap)
        font = ImageFont.truetype('arial.ttf', font_size)
        with Image.open("world.png") as img:
            draw = ImageDraw.Draw(img)
            text_w, text_h = draw.textsize(txt, font)
            if pos == 'n':
                start_pixel_x += (block_size - text_w) / 2
                start_pixel_y += gap / 2
            elif pos == 's':
                start_pixel_x += (block_size - text_w) / 2
                start_pixel_y += (block_size - gap * 3 / 2)
            elif pos == 'w':
                start_pixel_x += gap / 2
                start_pixel_y += (block_size - text_h) / 2 - text_h / 2
            elif pos == 'e':
                start_pixel_x += (block_size - text_w) - gap / 2
                start_pixel_y += (block_size - text_h) / 2 + text_h / 2
            else:
                start_pixel_x += (block_size - text_w) / 2
                start_pixel_y += (block_size - text_h) / 2
            draw.text((start_pixel_x + 1, start_pixel_y + 1), txt, fill=t_color, font=font)
            img.save('world.png')

    def put_x(self, coor=(0, 0), color='white'):
        x = coor[0]
        y = coor[1]
        start_pixel_x = gap + x * (block_size + gap)
        start_pixel_y = gap + y * (block_size + gap)
        with Image.open("world.png") as img:
            draw = ImageDraw.Draw(img)
            draw.line([(start_pixel_x + 1, start_pixel_y + 1),
                       (start_pixel_x + 99, start_pixel_y + 99)], fill=color, width=0)
            draw.line([(start_pixel_x + 1, start_pixel_y + 99),
                       (start_pixel_x + 99, start_pixel_y + 1)], fill=color, width=0)
        img.save('world.png')