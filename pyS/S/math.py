import math
import operator
from functools import reduce
from itertools import count

def product(nums):
    """Returns the product of all values

    Attributes:
        nums (iterable) Iterator of intergers
    """
    return reduce(operator.mul, nums, 1)

def is_prime(num):
    """Returns True if `num` is prime
    """
    if num < 2: return False

    for x in range(2, num):
        if num % x == 0:
            return False
    return True

def primes():
    """Returns an iterator of all primes number
    """
    return (x for x in count() if is_prime(x))

def factorize(num):
    """Factorization in primes of a number

    Attributes:
        num (int) Number to factorize

    Returns:
        An interator that returns every powers of the factorization

    Examples:
        >>> list(factorize(126)) == [1, 2, 0, 1] # 2**1 * 3**2 * 5**0 * 7**1 = 126
    """
    for p in primes():
        if p > num: return
        c = 0
        while num % p == 0:
            num //= p
            c += 1
        yield c
