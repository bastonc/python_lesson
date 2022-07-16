import math


class Shape:  # class Shape(object)

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def square(self):
        return 0


class Circles(Shape):

    def __init__(self, x, y, radius):
        super().__init__(x, y)
        self.radius = radius

    def square(self):
        return math.pi * self.radius ** 2


class Rectangle(Shape):

    def __init__(self, x, y, height, width):
        super().__init__(x, y)
        self.height = height
        self.width = width

    def square(self):
        return self.width * self.height


class Parallelogram(Rectangle):

    def __init__(self, x, y, height, width, angle):
        super().__init__(x, y, height, width)
        self.angle = angle

    def square(self):
        return self.width * self.height * math.sin(self.angle)

    def print_angle(self):
        print(self.angle)

    def __str__(self):
        result = super().__str__()
        return result + f'\nParallelogram: {self.width}, {self.height}, {self.angle}'

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class Triangle(Shape):

    def __init__(self, x, y, long_edge):
        super().__init__(x, y)
        self.long_edge = long_edge

    def square(self):
        p = (self.long_edge * 3) / 2
        s1 = math.sqrt(p * (p - self.long_edge) * (p - self.long_edge) * (p - self.long_edge))
        s2 = math.sqrt(p * (p - self.long_edge) ** 3)
        return s1


class Scene:
    def __init__(self):
        self._figures = []

    def add_figure(self, figure):
        self._figures.append(figure)

    def total_square(self):
        return sum(f.square() for f in self._figures)

    def __str__(self):
        pass



