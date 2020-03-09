from geometry import Circle
from geometry import Point
import math


def test_point_creation():
    p1 = Point(1, 2)
    assert p1 != None


def test_point_distance():
    p1 = Point(-2, 2)
    p2 = Point(3, -3)
    dist = Point.get_distance(p1, p2)
    assert p1 != None
    assert p2 != None
    assert dist == 7.0710678118654755


def test_get_point_between_points():
    p1 = Point(4, 5)
    p2 = Point(20, 25)
    p3 = Point(30, 6)
    p = Point.get_point_between_points(p1, p2, p3)
    assert p1 != None
    assert p2 != None
    assert p3 != None
    assert p != None
    assert p.x == 18
    assert p.y == 12


def test_circle_creation():
    c1 = Circle(-4, -2, 2)
    c2 = Circle(1, -2, 3)
    assert c1 != None
    assert c2 != None


def test_min_circles_distance():
    c1 = Circle(-4, -2, 2)
    c2 = Circle(1, -2, 3)
    min = Circle.get_min_distance(c1, c2)
    hit = Circle.is_min_hit(c1, c2)
    assert c1 != None
    assert c2 != None
    assert min == -2.0710678118654755
    assert hit == True


def test_max_circles_distance():
    c1 = Circle(-4, -2, 2)
    c2 = Circle(1, -2, 3)
    max = Circle.get_max_distance(c1, c2)
    hit = Circle.is_max_hit(c1, c2)
    assert c1 != None
    assert c2 != None
    assert max == 0
    assert hit == False


def test_avg_circles_distance():
    c1 = Circle(-4, -2, 2)
    c2 = Circle(1, -2, 3)
    avg = Circle.get_avg_distance(c1, c2)
    hit = Circle.is_avg_hit(c1, c2)
    assert c1 != None
    assert c2 != None
    assert avg == -1.0355339059327378
    assert hit == True


def test_get_available_min_radius():
    c1 = Circle(-4, -2, 2)
    c2 = Circle(1, -2, 3)
    radius = Circle.get_available_min_radius(c1, [c2])
    assert radius == 0.7573593128807143
    radius = Circle.get_available_min_radius(c2, [c1])
    assert radius == 2.1715728752538097


def test_get_available_max_radius():
    c1 = Circle(-4, -2, 2)
    c2 = Circle(1, -2, 3)
    radius = Circle.get_available_max_radius(c1, [c2])
    assert radius == 2.0
    radius = Circle.get_available_max_radius(c2, [c1])
    assert radius == 3.0


def test_get_circle_between_3points():
    p1 = Point(4, 5)
    p2 = Point(20, 25)
    p3 = Point(30, 6)
    c = Circle.get_circle_between_3points(p1, p2, p3)
    assert p1 != None
    assert p2 != None
    assert p3 != None
    assert c != None
    assert c.x == 18
    assert c.y == 12
    assert c.r == 15.652475842498529


def test_get_inner_circle_point_between_0_and_corner_TR():
    # top right corner
    c = Circle(3, 3, 1)
    p = Point(0, 0)
    r = Circle.get_circle_point(c, p, outer=False)
    assert c != None
    assert p != None
    assert r != None
    assert r.x == 2.2928932188134525
    assert r.y == 2.2928932188134525
    # same horizontal level
    c = Circle(3, 3, 1)
    p = Point(0, 3)
    r = Circle.get_circle_point(c, p, outer=False)
    assert c != None
    assert p != None
    assert r != None
    assert r.x == 2
    assert r.y == 3
    # same vertical level
    c = Circle(3, 3, 1)
    p = Point(3, 0)
    r = Circle.get_circle_point(c, p, outer=False)
    assert c != None
    assert p != None
    assert r != None
    assert r.x == 3
    assert r.y == 2


def test_get_inner_circle_point_between_0_and_corner_BR():
    # bottom right corner
    c = Circle(3, -3, 1)
    p = Point(0, 0)
    r = Circle.get_circle_point(c, p, outer=False)
    assert c != None
    assert p != None
    assert r != None
    assert r.x == 2.2928932188134525
    assert r.y == -2.2928932188134525
    # same horizontal level
    c = Circle(3, -3, 1)
    p = Point(0, -3)
    r = Circle.get_circle_point(c, p, outer=False)
    assert c != None
    assert p != None
    assert r != None
    assert r.x == 2
    assert r.y == -3
    # same vertical level
    c = Circle(3, -3, 1)
    p = Point(3, 0)
    r = Circle.get_circle_point(c, p, outer=False)
    assert c != None
    assert p != None
    assert r != None
    assert r.x == 3
    assert r.y == -2


def test_get_inner_circle_point_between_0_and_corner_TL():
    # top left corner
    c = Circle(-3, 3, 1)
    p = Point(0, 0)
    r = Circle.get_circle_point(c, p, outer=False)
    assert c != None
    assert p != None
    assert r != None
    assert r.x == -2.2928932188134525
    assert r.y == 2.2928932188134525
    # same horizontal level
    c = Circle(-3, 3, 1)
    p = Point(0, 3)
    r = Circle.get_circle_point(c, p, outer=False)
    assert c != None
    assert p != None
    assert r != None
    assert r.x == -2
    assert r.y == 3
    # same vertical level
    c = Circle(-3, 3, 1)
    p = Point(-3, 0)
    r = Circle.get_circle_point(c, p, outer=False)
    assert c != None
    assert p != None
    assert r != None
    assert r.x == -3
    assert r.y == 2


def test_get_inner_circle_point_between_0_and_corner_BL():
    # bottm right corner
    c = Circle(-3, -3, 1)
    p = Point(0, 0)
    r = Circle.get_circle_point(c, p, outer=False)
    assert c != None
    assert p != None
    assert r != None
    assert r.x == -2.292893218813452
    assert r.y == -2.2928932188134525
    # same horizontal level
    c = Circle(-3, -3, 1)
    p = Point(-3, 0)
    r = Circle.get_circle_point(c, p, outer=False)
    assert c != None
    assert p != None
    assert r != None
    assert r.x == -3
    assert r.y == -2
    # same vertical level
    c = Circle(-3, -3, 1)
    p = Point(0, -3)
    r = Circle.get_circle_point(c, p, outer=False)
    assert c != None
    assert p != None
    assert r != None
    assert r.x == -2
    assert r.y == -3
