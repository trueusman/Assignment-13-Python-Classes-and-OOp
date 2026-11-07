"""Task 12: Range-like iterable with reverse, length and membership."""

class ReversibleRange:
    def __init__(self, start, stop, step=1):
        if not all(isinstance(v, int) and not isinstance(v, bool)
                   for v in (start, stop, step)):
            raise TypeError("start, stop and step must be integers")
        if step == 0:
            raise ValueError("step cannot be zero")
        self.start, self.stop, self.step = start, stop, step

    def __iter__(self):
        current = self.start
        if self.step > 0:
            while current < self.stop:
                yield current
                current += self.step
        else:
            while current > self.stop:
                yield current
                current += self.step

    def __len__(self):
        if self.step > 0:
            return max(0, (self.stop - self.start + self.step - 1) // self.step)
        step = -self.step
        return max(0, (self.start - self.stop + step - 1) // step)

    def __reversed__(self):
        length = len(self)
        if length:
            last = self.start + (length - 1) * self.step
            current = last
            for _ in range(length):
                yield current
                current -= self.step

    def __contains__(self, value):
        if not isinstance(value, int) or isinstance(value, bool):
            return False
        if self.step > 0:
            in_bounds = self.start <= value < self.stop
        else:
            in_bounds = self.stop < value <= self.start
        return in_bounds and (value - self.start) % self.step == 0


if __name__ == "__main__":
    values = ReversibleRange(2, 11, 3)
    print(list(values), list(reversed(values)), len(values), 5 in values)
