
from __future__ import division, print_function, unicode_literals

"""
Test Examples
=============


## Python Tests
self.assertTrue(value)
self.assertFalse(value)

self.assertGreater(first, second, msg=None)
self.assertGreaterEqual(first, second, msg=None)
self.assertLess(first, second, msg=None)
self.assertLessEqual(first, second, msg=None)

self.assertAlmostEqual(first, second, places=7, msg=None, delta=None)
self.assertNotAlmostEqual(first, second, places=7, msg=None, delta=None)

self.assertItemsEqual(actual, expected, msg=None)
self.assertSequenceEqual(seq1, seq2, msg=None, seq_type=None)
self.assertListEqual(list1, list2, msg=None)
self.assertTupleEqual(tuple1, tuple2, msg=None)
self.assertSetEqual(set1, set2, msg=None)
self.assertDictEqual(expected, actual, msg=None)

self.assertRaises(Exception, some_func, arg, arg_nother)

"""

import unittest
import os
import pathlib

import context

from snail import device

_path_module = pathlib.Path(__file__).parent.absolute()


#------------------------------------------------

class TestBits(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass


    def test_number_of_bits(self):
        self.assertTrue(device.number_of_bits(0) == 0)
        self.assertTrue(device.number_of_bits(1) == 1)
        self.assertTrue(device.number_of_bits(2) == 2)
        self.assertTrue(device.number_of_bits(3) == 2)
        self.assertTrue(device.number_of_bits(255) == 8)
        self.assertTrue(device.number_of_bits(256) == 9)

    def test_number_of_bytes(self):
        self.assertTrue(device.number_of_bytes(0) == 0)
        self.assertTrue(device.number_of_bytes(3) == 1)
        self.assertTrue(device.number_of_bytes(255) == 1)
        self.assertTrue(device.number_of_bytes(256) == 2)

    def test_mask_a(self):
        MSB = 1
        LSB = 0
        tst = device.mask(MSB, LSB)
        val = 0b11
        self.assertTrue(tst == val, (tst, val))

    def test_mask_b(self):
        MSB = 1
        LSB = 1
        tst = device.mask(MSB, LSB)
        val = 0b10
        self.assertTrue(tst == val, (tst, val))

    def test_mask_c(self):
        MSB = 5
        LSB = 2
        tst = device.mask(MSB, LSB)
        val = 0b00111100
        self.assertTrue(tst == val, (tst, val))

    def test_mask_d(self):
        MSB = 0
        LSB = 0
        tst = device.mask(MSB, LSB)
        val = 1
        self.assertTrue(tst == val, (tst, val))

    def test_mask_e(self):
        MSB = 7
        LSB = 0
        tst = device.mask(MSB, LSB)
        val = 255
        self.assertTrue(tst == val, (tst, val))


#------------------------------------------------
if __name__ == '__main__':
    unittest.main(verbosity=2)
