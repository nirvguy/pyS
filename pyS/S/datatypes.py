from .math import product, primes, factorize

class SInt:
    """S Integer datatype
    """
    def __init__(self, z):
        """
        Constructor
        """
        if isinstance(z, SInt):
            self.z = z.z
        elif isinstance(z, int):
            self.z = z
        else:
            raise Exception("wrong type")

    def decode(self):
        return self.z

    @staticmethod
    def encode(x):
        return SInt(self.z)

    def __str__(self):
        return str(self.decode())

class STuple(SInt):
    """S tuple datatype
    """

    def __init__(self, z):
        """Constructor
        """
        SInt.__init__(self, z)

    def decode(self):
        """Decodes a S tuple into a Python tuple
        """
        x = self.l()
        y = ((self.z + 1) // 2 ** x - 1) // 2
        return (x, y)

    def l(self):
        """Gets the lefthand number of the S tuple
        """
        return max(range(0, self.z + 1),
                   key=lambda t: t if (self.z + 1) % 2**t == 0 else 0)

    def r(self):
        """Gets the righthand number of the S tuple
        """
        return max(range(0, self.z + 1),
                   key=lambda t: t if (self.z + 1) % (2*t + 1) == 0 else 0)

    @staticmethod
    def encode(v):
        """Encodes tuple (x,y) into a S tuple
        """
        return STuple(2**v[0] * (2 * v[1] + 1) - 1)

class SList(SInt):
    """S list data type
    """

    def __init__(self, z):
        """Constructor
        """
        SInt.__init__(self, z)

    def decode(self):
        """Decodes a S list into a values iterator
        """
        return factorize(self.z)

    @staticmethod
    def encode(zs):
        """Encodes a list of numbers into a S list
        """
        return SList(product((x[0] ** x[1] for x in zip(primes(), zs))))

    def __str__(self):
        return str(list(map(str, list(self.decode()))))
