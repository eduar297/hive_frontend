from math import *


class Point:
    def __init__(self, x=0, y=0):
        self.point = (x, y)
        self.x, self.y = x, y

    def translate(self, x, y):
        self.x, self.y = x, y

    def __str__(self):
        return f'({self.x},{self.y})'


class Hexagon:
    def __init__(self, center, size, hex=None, color=None, value=None):
        self.center, self.size = center, size
        self.w = sqrt(3)*size
        self.h = 2*size
        self.p1 = self.pointy_hex_corner(center, 0)
        self.p2 = self.pointy_hex_corner(center, 1)
        self.p3 = self.pointy_hex_corner(center, 2)
        self.p4 = self.pointy_hex_corner(center, 3)
        self.p5 = self.pointy_hex_corner(center, 4)
        self.p6 = self.pointy_hex_corner(center, 5)
        self.points = [self.p1.point, self.p2.point, self.p3.point,
                       self.p4.point, self.p5.point, self.p6.point]
        self.hex = hex
        self.color = color
        self.value = value

    def update(self, center=None, size=None, hex=None, color=None, value=None):
        if center:
            self.center = center
            self.p1 = self.pointy_hex_corner(center, 0)
            self.p2 = self.pointy_hex_corner(center, 1)
            self.p3 = self.pointy_hex_corner(center, 2)
            self.p4 = self.pointy_hex_corner(center, 3)
            self.p5 = self.pointy_hex_corner(center, 4)
            self.p6 = self.pointy_hex_corner(center, 5)
            self.points = [self.p1.point, self.p2.point, self.p3.point,
                           self.p4.point, self.p5.point, self.p6.point]
        if size:
            self.size = size
            self.w = sqrt(3)*size
            self.h = 2*size
        if hex:
            self.hex = hex
        if color:
            self.color = color
        if value:
            self.value = value

    def pointy_hex_corner(self, center, i):
        angle_deg = 60 * i - 30
        angle_rad = pi / 180 * angle_deg
        return Point(center.x + self.size * cos(angle_rad),
                     center.y + self.size * sin(angle_rad))

    def copy(self):
        if self != None:
            return Hexagon(self.center, self.size, self.hex, self.color)
        else:
            return None


class Cube:
    def __init__(self, x=0, y=0, z=0):
        self.x, self.y, self.z = x, y, z
        self.point = (x, y, z)

    def __str__(self):
        return f'({self.x},{self.y}, {self.z})'

    def cube_round(cube):
        rx = round(cube.x)
        ry = round(cube.y)
        rz = round(cube.z)
        x_diff = abs(rx - cube.x)
        y_diff = abs(ry - cube.y)
        z_diff = abs(rz - cube.z)

        if x_diff > y_diff and x_diff > z_diff:
            rx = -ry-rz
        elif y_diff > z_diff:
            ry = -rx-rz
        else:
            rz = -rx-ry

        return Cube(rx, ry, rz)


class Hex:
    def __init__(self, q=0, r=0):
        self.q, self.r = q, r
        self.point = Point(q, r)

    def __str__(self):
        return f'({self.q},{self.r})'

    def axial_directions(q1, q2, r1, r2):
        ad = []
        for _q in range(q1, q2+1):
            for _r in range(r1, r2+1):
                # ad.append(Hex.axial_to_oddr(Hex(_q, _r)))
                ad.append(Hex(_q, _r))
        return ad

    def oddr_offset_to_pixel(hex, size):
        x = size * sqrt(3) * (hex.q + 0.5 * (hex.r & 1))
        y = size * 3/2 * hex.r
        return Point(x, y)

    def pixel_to_pointy_hex(point, size):
        q = (sqrt(3)/3 * point.x - 1/3 * point.y) / size
        r = (2/3 * point.y) / size
        return Hex.hex_round(Hex(q, r))

    def pointy_hex_to_pixel(hex, size):
        x = size * (sqrt(3) * hex.q + sqrt(3)/2 * hex.r)
        y = size * (3./2 * hex.r)
        return Point(x, y)

    def hex_round(hex):
        # return Hex.cube_to_oddr(Cube.cube_round(Hex.axial_to_cube(hex)))
        return Hex.cube_to_axial(Cube.cube_round(Hex.axial_to_cube(hex)))

    def cube_to_axial(cube):
        q = cube.x
        r = cube.z
        return Hex(q, r)

    def axial_to_cube(hex):
        x = hex.q
        z = hex.r
        y = -x-z
        return Cube(x, y, z)

    def cube_to_oddr(cube):
        q = cube.x + (cube.z - (cube.z & 1)) // 2
        r = cube.z
        return Hex(q, r)

    def oddr_to_cube(hex):
        q = hex.q - (hex.r - (hex.r & 1)) // 2
        r = hex.r
        s = -q-r
        return Cube(q, r, s)

    def axial_to_oddr(hex):
        col = hex.q + (hex.r - (hex.r & 1)) // 2
        row = hex.r
        return Hex(col, row)

    def oddr_to_axial(hex):
        q = hex.q - (hex.r - (hex.r & 1)) // 2
        r = hex.r
        return Hex(q, r)
