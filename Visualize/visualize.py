from PIL import Image, ImageDraw, ImageFont

gap = 7
block_size = 65
font_size = 18


class Visualize:
    def __init__(self, name):
        self.name = name

    # generate world image
    def visualize_gen(self, num_cell_h, num_cell_w):
        f_name = self.name
        img_h = num_cell_h * (block_size + gap) + gap
        img_w = num_cell_w * (block_size + gap) + gap

        img = Image.new('RGB', (img_w, img_h), color='gray')
        draw = ImageDraw.Draw(img)

        # row divider
        for r in range(num_cell_h + 1):
            start_p_r = (block_size + gap) * r + gap / 2
            draw.line([(0, start_p_r), (img_w, start_p_r)], fill=0, width=gap + 1)
        # col divider
        for r in range(num_cell_w + 1):
            start_p_c = (block_size + gap) * r + gap / 2
            draw.line([(start_p_c, 0), (start_p_c, img_h)], fill=0, width=gap + 1)

        img.save('Images/%s.png' % f_name)

    def fill_block(self, coor=(0, 0), color='white'):
        f_name = self.name
        x = coor[0]
        y = coor[1]
        start_pixel_x = gap + x * (block_size + gap)
        start_pixel_y = gap + y * (block_size + gap)
        with Image.open('Images/%s.png' % f_name) as img:
            draw = ImageDraw.Draw(img)
            draw.rectangle((start_pixel_x + 1, start_pixel_y + 1,
                            start_pixel_x + block_size - 0.5, start_pixel_y + block_size - 0.5),
                           fill=color)
            img.save('Images/%s.png' % f_name)

    def write_block(self, coor=(0, 0), txt='text', t_color='white',
                    pos='c', font_s=font_size, offset_u=0, offset_d=0, offset_l=0, offset_r=0):
        f_name = self.name
        x = coor[0]
        y = coor[1]
        start_pixel_x = gap + x * (block_size + gap)
        start_pixel_y = gap + y * (block_size + gap)
        try:
            font = ImageFont.truetype(r'arial.ttf', font_s)
        except:
            font = ImageFont.load_default()

        with Image.open('Images/%s.png' % f_name) as img:
            draw = ImageDraw.Draw(img)
            text_w, text_h = draw.textsize(txt, font)
            if pos == 'n':
                start_pixel_x += (block_size - text_w) / 2 + offset_r - offset_l
                start_pixel_y += gap - offset_u + offset_d
            elif pos == 's':
                start_pixel_x += (block_size - text_w) / 2 + offset_r - offset_l
                start_pixel_y += (block_size - gap * 3 / 2) - text_h / 2 - offset_u + offset_d
            elif pos == 'w':
                start_pixel_x += gap / 2 + offset_r - offset_l
                start_pixel_y += (block_size - text_h) / 2 - text_h / 2 - offset_u + offset_d
            elif pos == 'e':
                start_pixel_x += (block_size - text_w) - gap / 2 + offset_r - offset_l
                start_pixel_y += (block_size - text_h) / 2 + text_h / 2 - offset_u + offset_d
            else:
                start_pixel_x += (block_size - text_w) / 2 + offset_r - offset_l
                start_pixel_y += (block_size - text_h) / 2 - offset_u + offset_d
            draw.text((start_pixel_x + 1, start_pixel_y + 1), txt, fill=t_color, font=font)
            img.save('Images/%s.png' % f_name)

    def put_x(self, coor=(0, 0), color='white'):
        f_name = self.name
        x = coor[0]
        y = coor[1]
        start_pixel_x = gap + x * (block_size + gap)
        start_pixel_y = gap + y * (block_size + gap)
        with Image.open('Images/%s.png' % f_name) as img:
            draw = ImageDraw.Draw(img)
            draw.line([(start_pixel_x + 1, start_pixel_y + 1),
                       (start_pixel_x + block_size - 1, start_pixel_y + block_size - 1)], fill=color, width=0)
            draw.line([(start_pixel_x + 1, start_pixel_y + block_size - 1),
                       (start_pixel_x + block_size - 1, start_pixel_y + 1)], fill=color, width=0)
        img.save('Images/%s.png' % f_name)

    def get_color(self, x, y):
        f_name = self.name
        start_pixel_x = gap + x * (block_size + gap) + 2
        start_pixel_y = gap + y * (block_size + gap) + 1
        with Image.open('Images/%s.png' % f_name) as img:
            img_rgb = img.convert("RGB")
            color = img_rgb.getpixel((start_pixel_x, start_pixel_y))
        r = color[0]
        g = color[1]
        b = color[2]
        return r, g, b

    def snapshot(self, name):
        f_name = self.name
        with Image.open('Images/%s.png' % f_name) as img:
            snapshot = img.copy()
            snapshot.save('Images/%s.png' % name)
