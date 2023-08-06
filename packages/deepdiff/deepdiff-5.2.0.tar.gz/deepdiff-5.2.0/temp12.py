from deepdiff import DeepDiff, Delta


class CustomClass:
    def __init__(self, a, b=None):
        self.a = a
        self.b = b

    def __str__(self):
        return "Custom({}, {})".format(self.a, self.b)

    __repr__ = __str__


t1 = CustomClass(a=10, b=10)
t2 = CustomClass(a=10, b=12)

diff = DeepDiff(t1, t2)

delta = Delta(diff)

t1
t2
t3 = t1 + delta
t3
