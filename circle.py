
class Circle:
    def __init__(self, x: int, y: int, radius: int):
        self.x = x
        self.y = y
        self.radius = radius
        self.iter_count = self.x

    def __contains__(self, item):
        if abs(item.x - self.x) <= self.radius and abs(item.y - self.y) <= self.radius:
            return True
        else:
            return False