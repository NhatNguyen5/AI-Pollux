from PIL import Image, ImageDraw, ImageFont
from WorldProcessing.readWorld import ReadWorld

gap = 12
block_size = 100
font_size = 20


class Visualize:
    def __init__(self):
        pass

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
