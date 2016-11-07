#!/usr/bin/env python3
import sys
import unittest
import itertools

sys.path.append('..')

from pyS.S.datatypes import STuple, SList

class TestSTuple(unittest.TestCase):
    RANGE_X = 20
    RANGE_Y = 20
    RANGE = RANGE_X * RANGE_Y

    def test_decode_encode(self):
        for i in range(0, TestSTuple.RANGE):
            self.assertEqual(STuple.encode(STuple(i).decode()).z, i)

    def test_encode_decode(self):
        for x in range(0, TestSTuple.RANGE_X):
            for y in range(0, TestSTuple.RANGE_Y):
                self.assertEqual(STuple.encode((x,y)).decode(),(x,y))


def all_sequences(k, elems):
    return (l for i in range(0, k+1) for l in product(elems, repeat=i))

class TestSList(unittest.TestCase):
    RANGE = 1000
    RANGE_N = 5
    RANGE_K = 8

    def test_decode_encode(self):
        for i in range(1, TestSList.RANGE):
            self.assertEqual(SList.encode(SList(i).decode()).z, i)

    def test_encode_decode(self):
        for l in all_sequences(TestSList.RANGE_K, range(1, TestSList.RANGE_N)):
            self.assertEqual(list(SList.encode(l).decode()),l)

if __name__ == '__main__':
    unittest.main()
