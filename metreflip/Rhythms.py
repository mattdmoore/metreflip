from sympy.utilities.iterables import necklaces


class Rhythms(list):
    def __init__(self, n, k=2):
        super().__init__(Rhythm(r[::-1]) for r in necklaces(n, k))

    def __repr__(self):
        return '\n'.join([str(rhythm) for rhythm in self])


class Rhythm(list):
    def __init__(self, rhythm: tuple | list):
        if not any(rhythm):  # empty set
            super().__init__(rhythm)
            self.durations = self
        elif max(rhythm) > 1:  # from durations
            super().__init__([int(not i) for v in rhythm for i in range(v)])
            self.durations = rhythm
        else:  # from positions
            result = []
            i = 0
            for v in rhythm[::-1]:
                if v:
                    result.append(i + 1)
                    i = 0
                else:
                    i += 1
            result[0] += i
            super().__init__(rhythm)
            self.durations = tuple(result[::-1])

    def __and__(self, other):
        return Rhythm([a & b for a, b in zip(self, other)])

    def __xor__(self, other):
        return Rhythm([a ^ b for a, b in zip(self, other)])

    def __index__(self):
        canonical = tuple(self.canonical_rotation())
        for i, necklace in enumerate(necklaces(len(self), 2)):
            if canonical == necklace[::-1]:
                return i

    def rotate(self, r):
        return Rhythm(self[r:] + self[:r])

    def canonical_rotation(self):
        if sum(self) == 0:
            return self
        as_string = ''.join(str(onset) for onset in self[::-1])
        min_num = int(as_string, 2)
        for _ in range(len(self)):
            if int(as_string := as_string[1:] + as_string[0], 2) < min_num:
                min_num = int(as_string, 2)
        result = bin(min_num)[2:].zfill(len(self))[::-1]
        return Rhythm([int(i) for i in result])
