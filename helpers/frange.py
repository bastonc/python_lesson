class Frange:

    def __init__(self, start, stop, step):
        self.start = float(start)
        self.stop = float(stop)
        self.step = float(step)
        self.result = self.start

    def __next__(self):
        self.out = self.result
        self.result += self.step
        if self.step < 0 and self.out <= self.stop:
            raise StopIteration
        if self.step >= 0 and self.out >= self.stop:
            raise StopIteration
        return self.out

    def __iter__(self):
        return self