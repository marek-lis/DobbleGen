import math


class Point:

    def __init__(self, x, y):
        self.__x = x
        self.__y = y

    def __str__(self):
        return "Point" + " x: " + '{:+0.3f}'.format(self.x) + " y: " + '{:+0.3f}'.format(self.y)

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    @staticmethod
    def get_distance(p1, p2):
        # calculate the distance between 2 points
        return math.sqrt(math.pow(p1.x - p2.x, 2) + math.pow(p1.y - p2.y, 2))

    @staticmethod
    def get_point_between_points(p1, p2, p3):
        # calculate parameters of a point located in the middle of p1, p2, p3
        # (calculations based on circle inside the square)
        x = (p1.x + p2.x + p3.x) / 3
        y = (p1.y + p2.y + p3.y) / 3
        return Point(x, y)


class Circle(Point):

    # based on http://www.matematykam.pl/wzajemne_polozenie_okregow_w_ukl_wpolrzednych.html

    def __init__(self, x, y, r, a=0):
        # position x in float (0.0-1.0)
        self.__x = x
        # position y in float (0.0-1.0)
        self.__y = y
        # radius in float (0.0-1.0)
        self.__r = r
        # rotation in degrees (0-360)
        self.__a = a

    def __str__(self):
        return "Circle" + " x: " + '{:+0.3f}'.format(self.x) + " y: " + '{:+0.3f}'.format(self.y) + " r: " + '{:+0.3f}'.format(self.r) + " a: " + '{:05.1f}'.format(self.a)

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    @property
    def r(self):
        return self.__r

    @property
    def a(self):
        return self.__a

    @a.setter
    def a(self, val):
        self.__a = val % 360

    @staticmethod
    def get_max_distance(c1, c2):
        # calculate the distance between 2 circles - both minimum radiuses
        # (calculations based on circle inside the square)
        return math.sqrt(math.pow(c1.x - c2.x, 2) + math.pow(c1.y - c2.y, 2)) - c1.r - c2.r

    @staticmethod
    def get_min_distance(c1, c2):
        # calculate the distance between 2 circles - both maximum radiuses (sqrt(2) * (r1 + r2))
        # (calculations based on circle outside a square)
        return math.sqrt(math.pow(c1.x - c2.x, 2) + math.pow(c1.y - c2.y, 2)) - (math.sqrt(2) * (c1.r + c2.r))

    @staticmethod
    def get_avg_distance(c1, c2):
        # average distance is min + (max - min) / 2
        min = Circle.get_min_distance(c1, c2)
        max = Circle.get_max_distance(c1, c2)
        return min + (max - min) / 2

    @staticmethod
    def is_min_hit(c1, c2):
        # check if 2 circles are closer than their minimum distance
        return Circle.get_min_distance(c1, c2) < 0

    @staticmethod
    def is_max_hit(c1, c2):
        # check if 2 circles are closer than their maximum distance
        return Circle.get_max_distance(c1, c2) < 0

    @staticmethod
    def is_avg_hit(c1, c2):
        # check if 2 circles are closer than their average distance
        return Circle.get_avg_distance(c1, c2) < 0

    @staticmethod
    def get_available_min_radius(circle, list_of_circles):
        # calculate such minimum radius length for circle c1 not to hit other circles from list_of_circles
        # (calculations based on circle outside a square)
        c = Circle(circle.x, circle.y, 0)
        return min([Circle.get_min_distance(c, item) for item in list_of_circles])

    @staticmethod
    def get_available_avg_radius(circle, list_of_circles):
        # calculate such avg radius length for circle c1 not to hit other circles from list_of_circles
        # (calculations based on circle outside a square)
        c = Circle(circle.x, circle.y, 0)
        return min([Circle.get_avg_distance(c, item) for item in list_of_circles])

    @staticmethod
    def get_available_max_radius(circle, list_of_circles):
        # calculate such maximum radius length for circle c1 not to hit other circles from list_of_circles
        # (calculations based on circle inside the square)
        c = Circle(circle.x, circle.y, 0)
        return min([Circle.get_max_distance(c, item) for item in list_of_circles])

    @staticmethod
    def get_circle_between_3points(p1, p2, p3):
        # calculate parameters of a new circle located in the middle of p1, p2, p3
        # (calculations based on circle inside the square)
        x = (p1.x + p2.x + p3.x) / 3
        y = (p1.y + p2.y + p3.y) / 3
        r = Point.get_distance(p1, Point(x, y))
        return Circle(x, y, r)

    @staticmethod
    def get_circle_between_2points(p1, p2):
        # calculate parameters of a new circle located in the middle of p1, p2
        # (calculations based on circle inside the square)
        x = (p1.x + p2.x) / 2
        y = (p1.y + p2.y) / 2
        r = Point.get_distance(p1, Point(x, y))
        return Circle(x, y, r)

    @staticmethod
    def get_circle_point(c, p, outer=True):
        # calculate location of a point on given circle c in the direction to point p
        # y = ax + b
        # tg(alpha) = a = (y2 - y1) / (x2 - x1)
        # alpha = arctg(a)
        # if outer == True then we calculate the outer circle radius:
        # r = square(2) * c.r, otherwise, we use inner circle radius: c.r
        # x = r * cos(alpha)
        # y = r * sin(alpha)
        dx, dy = c.x - p.x, c.y - p.y
        if dx == 0:
            dx = 0.0000000000000000000000000000000001
        a = dy / dx
        alpha = math.atan(a)
        if (c.x < p.x):
            alpha += math.pi
        r = c.r
        if outer == True:
            r *= math.sqrt(2)
        x = r * math.cos(alpha)
        y = r * math.sin(alpha)
        return Point(c.x - x, c.y - y)

    @staticmethod
    def get_circle_points(points_num):
        # calculate the location 360/angle_per_point points on a circle with radius 1
        # square: 360 / 90 = 4 points
        # triangle: 360 / 135 = 3 points
        angle_per_point = 360/points_num
        return [Point(math.sin(
            math.radians(point_num * angle_per_point)),
            math.cos(math.radians(point_num * angle_per_point)))
            for point_num in range(points_num)]


class Triangle(Point):

    def __init__(self, points):
        self.__points = points

    def __str__(self):
        result = "Triangle: "
        for point in self.__points:
            result += (point.__str__() + " ")
        return result

    @property
    def points(self):
        return self.__points

    @staticmethod
    def new():
        return Triangle(Circle.get_circle_points(3))


class Trapeze(Point):

    def __init__(self, points):
        self.__points = points

    def __str__(self):
        result = "Trapeze: "
        for point in self.__points:
            result += (point.__str__() + " ")
        return result

    @property
    def points(self):
        return self.__points

    @staticmethod
    def new():
        return Trapeze(Circle.get_circle_points(5)[1:5])


class Rhombus(Point):

    def __init__(self, points):
        self.__points = points

    def __str__(self):
        result = "Rhombus: "
        for point in self.__points:
            result += (point.__str__() + " ")
        return result

    @property
    def points(self):
        return self.__points

    @staticmethod
    def new():
        points = Circle.get_circle_points(5)[1:4]
        points.append(Point(-0.2, points[0].y))
        return Rhombus(points)


class Square(Point):

    def __init__(self, points):
        self.__points = points

    def __str__(self):
        result = "Square: "
        for point in self.__points:
            result += (point.__str__() + " ")
        return result

    @property
    def points(self):
        return self.__points

    @staticmethod
    def new():
        return Square(Circle.get_circle_points(4))


class Pentagon(Point):

    def __init__(self, points):
        self.__points = points

    def __str__(self):
        result = "Pentagon: "
        for point in self.__points:
            result += (point.__str__() + " ")
        return result

    @property
    def points(self):
        return self.__points

    @staticmethod
    def new():
        return Pentagon(Circle.get_circle_points(5))


class Hexagon(Point):

    def __init__(self, points):
        self.__points = points

    def __str__(self):
        result = "Hexagon: "
        for point in self.__points:
            result += (point.__str__() + " ")
        return result

    @property
    def points(self):
        return self.__points

    @staticmethod
    def new():
        return Hexagon(Circle.get_circle_points(6))


class Septagon(Point):

    def __init__(self, points):
        self.__points = points

    def __str__(self):
        result = "Septagon: "
        for point in self.__points:
            result += (point.__str__() + " ")
        return result

    @property
    def points(self):
        return self.__points

    @staticmethod
    def new():
        return Septagon(Circle.get_circle_points(7))


class Octagon(Point):

    def __init__(self, points):
        self.__points = points

    def __str__(self):
        result = "Septagon: "
        for point in self.__points:
            result += (point.__str__() + " ")
        return result

    @property
    def points(self):
        return self.__points

    @staticmethod
    def new():
        return Octagon(Circle.get_circle_points(8))


class Ntagon(Point):

    def __init__(self, points):
        self.__points = points

    def __str__(self):
        result = "Ntagon: "
        for point in self.__points:
            result += (point.__str__() + " ")
        return result

    @property
    def points(self):
        return self.__points

    @staticmethod
    def new(n):
        return Ntagon(Circle.get_circle_points(n))
