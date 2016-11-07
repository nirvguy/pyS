#!/usr/bin/env python3
import sys
import unittest

sys.path.append('..')

from pyS.S.datatypes import STuple

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

if __name__ == '__main__':
    unittest.main()
