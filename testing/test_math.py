#!/usr/bin/env python3
import sys
import unittest
from itertools import islice

sys.path.append("..")

from pyS.S import math
import primes_list

factorization_result = { 0 : [],
                         1 : [],
                         2 : [1],
                         3 : [0, 1],
                         4 : [2],
                         5 : [0, 0, 1],
                         6 : [1, 1],
                         7 : [0, 0, 0, 1],
                         8 : [3],
                         9 : [0, 2] }


class TestPrimes(unittest.TestCase):
    def test_is_prime(self):
        self.assertFalse(math.is_prime(0))
        self.assertFalse(math.is_prime(1))
        for i in range(0, len(primes_list.PRIMES)):
            p = primes_list.PRIMES[i]
            self.assertTrue(math.is_prime(primes_list.PRIMES[i]))
            if i < len(primes_list.PRIMES) - 1:
                pn = primes_list.PRIMES[i+1]
                for i in range(p+1,pn):
                    self.assertFalse(math.is_prime(i))
                self.assertTrue(math.is_prime(pn))

    def test_iter_primos(self):
        self.assertEqual(list(islice(math.primes(), 0, len(primes_list.PRIMES))),
                         primes_list.PRIMES)

    def test_factorizar(self):
        for n, l in factorization_result.items():
            self.assertEqual(list(math.factorize(n)), l)

if __name__ == '__main__':
    unittest.main()
