import math
import random
from geometry import Circle, Point


class Planner:

    @staticmethod
    def get_card_data_4x4(items_num):
        first_pass = []
        second_pass = []
        angle_per_item = math.pi * 2 / items_num
        # create every second item
        for i in range(0, items_num, 2):
            angle = i * angle_per_item
            x = math.sin(angle) * 0.6
            y = math.cos(angle) * 0.6
            radius = random.uniform(0.10, 0.25)
            rotation = random.randrange(0, 360, 1)
            c = Circle(x, y, radius, rotation)
            first_pass.append(c)
            print(c)
        middle = Point(0, 0)
        first_pass_len = len(first_pass)
        # create all missing items
        for i in range(first_pass_len):
            c0 = first_pass[i]
            c1 = first_pass[(i+1) % first_pass_len]
            p0 = Circle.get_circle_point(c0, c1, outer=False)
            p1 = Circle.get_circle_point(c1, c0, outer=False)
            c = Circle.get_circle_between_2points(p0, p1)
            c.a = random.randrange(0, 360, 1)
            second_pass.append(c)
        # combine 2 lists of items into 1
        final = first_pass + second_pass
        return final

    @staticmethod
    def get_card_data_1x7(items_num):
        middle = Circle(0, 0, random.uniform(0.20, 0.25),
                        random.randrange(0, 360, 1))
        angle_per_item = 2 * math.pi / (items_num-1)
        radius = random.uniform(0.15, 0.20)
        rotation = random.randrange(0, 360, 1)
        angle = 0
        r = random.uniform(0.45, 0.55)
        x = math.sin(angle) * r
        y = math.cos(angle) * r
        first = Circle(x, y, radius, rotation)
        result = [middle] + [first]
        for i in range(items_num - 2):
            print(i)
            if i < 8:
                angle = (i+1) * angle_per_item
                rotation = random.randrange(0, 360, 1)
                r = random.uniform(0.45, 0.55)
                x = math.sin(angle) * r
                y = math.cos(angle) * r
                p0 = Point(x, y)
                radius = Circle.get_available_max_radius(
                    p0, [result[0], result[1+i], result[1]])
                radius -= (r - 0.45)
                radius = min(radius, 0.25)
                print(radius)
                c = Circle(x, y, radius, rotation)
                result.append(c)
        return result
