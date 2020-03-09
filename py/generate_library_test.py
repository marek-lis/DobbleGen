import os
import math
from random import randrange
from PIL import Image, ImageDraw


class Test_Pics:

    def __init__(self):
        pass

    def __rgb2hex(self, r, g, b):
        return '#{:02x}{:02x}{:02x}'.format(r, g, b)

    def __rgba2hex(self, r, g, b, a):
        return '#{:02x}{:02x}{:02x}{:02x}'.format(r, g, b, a)

    def create(self, path, num):
        image = Image.new('RGBA', (256, 256))
        rect_color = self.__rgb2hex(
            randrange(0, 255), randrange(0, 255), randrange(0, 255))
        background = ImageDraw.Draw(image)
        background.rectangle(
            ((0, 0), (image.width-1, image.height-1)), fill=rect_color, outline='#000000')
        circle_color = self.__rgb2hex(
            randrange(0, 255), randrange(0, 255), randrange(0, 255))
        background.ellipse(
            ((0, 0), (image.width-1, image.height-1)), fill=circle_color, outline='#000000')
        image.save(path + format(num, '02d') + '.png', dpi=(600, 600),
                   format='PNG', subsampling=0, quality=100)


icons_num = 57
output_path = 'lib/test/'
os.makedirs(output_path, exist_ok=True)
tp = Test_Pics()
for i in range(icons_num):
    tp.create(output_path, i)
