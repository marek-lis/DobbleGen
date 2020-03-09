import os
import math
from random import randrange
from PIL import Image, ImageDraw
from geometry import Circle, Trapeze, Rhombus, Triangle, Square, Pentagon, Hexagon, Septagon, Ntagon


class Geo_Pics:

    def __init__(self):
        self.__colors = {'black': '#000000', 'white': '#EFEFEF',
                         'red': '#FF2020', 'green': '#00FF00',
                         'blue': '#0000FF', 'pink': '#FF00FF',
                         'yellow': '#FFFF00', 'violet': '#7F00C0',
                         'orange': '#FFC000', 'brown': '#A43232'}
        self.__figures = ['circle', 'triangle',
                          'square', 'pentagon',
                          'rectangle', 'star', 'trapeze', 'rhombus']

    def __rgb2hex(self, r, g, b):
        return '#{:02x}{:02x}{:02x}'.format(r, g, b)

    def __rgba2hex(self, r, g, b, a):
        return '#{:02x}{:02x}{:02x}{:02x}'.format(r, g, b, a)

    def create(self, path):
        outline_color = '#000000'
        outline_width = 8
        num = 0
        for key, value in self.__colors.items():
            color = value
            for figure in self.__figures:
                image = Image.new('RGBA', (256, 256))
                background = ImageDraw.Draw(image)
                iw = image.width
                ih = image.height
                iw2 = round(iw/2)
                ih2 = round(ih/2)
                iw4 = round(iw2/2)
                ih4 = round(ih2/2)
                rw = iw2 - outline_width
                rh = ih2 - outline_width
                if figure == 'circle':
                    background.ellipse(
                        ((0, 0), (image.width-1, image.height-1)), fill=color, outline=outline_color, width=outline_width)
                elif figure == 'rectangle':
                    background.rectangle(
                        ((round(image.width/8), round(image.height/4)), (round(image.width-image.width/8-1), round(image.height-image.height/4)-1)), fill=color, outline=outline_color, width=outline_width)
                else:
                    if figure == 'star':
                        f = Ntagon.new(10)
                        i = 0
                        points = []
                        for p in f.points:
                            if i % 2 == 1:
                                rrw = iw4
                                rrh = ih4
                            else:
                                rrw = rw
                                rrh = rh
                            points.append(iw2 + p.x * rrw)
                            points.append(ih2 + p.y * rrh)
                            i += 1
                    elif figure == 'trapeze':
                        f = Trapeze.new()
                        points = []
                        for p in f.points:
                            points.append(iw2 + p.x * rw)
                            points.append(ih2 + p.y * rh)
                    elif figure == 'rhombus':
                        f = Rhombus.new()
                        points = []
                        for p in f.points:
                            points.append(iw2 + p.x * rw)
                            points.append(ih2 + p.y * rh)
                    elif figure == 'square':
                        f = Square.new()
                        points = []
                        for p in f.points:
                            points.append(iw2 + p.x * rw)
                            points.append(ih2 + p.y * rh)
                    elif figure == 'triangle':
                        f = Triangle.new()
                        points = []
                        for p in f.points:
                            points.append(iw2 + p.x * rw)
                            points.append(ih2 + p.y * rh)
                    elif figure == 'pentagon':
                        f = Pentagon.new()
                        points = []
                        for p in f.points:
                            points.append(iw2 + p.x * rw)
                            points.append(ih2 + p.y * rh)
                    elif figure == 'hexagon':
                        f = Hexagon.new()
                        points = []
                        for p in f.points:
                            points.append(iw2 + p.x * rw)
                            points.append(ih2 + p.y * rh)
                    background.polygon(points, fill=color,
                                       outline=outline_color)
                    points.append(points[0])
                    points.append(points[1])
                    background.line(points, fill=outline_color,
                                    width=outline_width)
                    for i in range(0, len(points), 2):
                        p1 = (round(points[i] - outline_width/3),
                              round(points[i+1] - outline_width/3))
                        p2 = (round(points[i] + outline_width/3),
                              round(points[i+1] + outline_width/3))
                        background.ellipse(
                            (p1, p2), fill=color, outline=outline_color, width=outline_width)
                num += 1
                image.save(path + format(num, '02d') + '.png', dpi=(600,
                                                                    600), format='PNG', subsampling=0, quality=100)


output_path = 'lib/geometry/'
os.makedirs(output_path, exist_ok=True)
gp = Geo_Pics()
gp.create(output_path)
