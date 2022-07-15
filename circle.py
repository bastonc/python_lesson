class Circle:
    def __init__(self, x: int, y: int, radius: int):
        self.x = x
        self.y = y
        self.radius = radius

    def contains(self, point: object):
        if abs(point.x - self.x) <= self.radius and abs(point.y - self.y) <= self.radius:
            return True
        return False
