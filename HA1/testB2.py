import unittest
from numpy.testing import assert_allclose
from B2 import *
import time

class TestB2(unittest.TestCase):
    def print_all(self, x_mean, width, u, k, c, start):
        print("Upper limit:", x_mean + width/2)
        print("Lower limit:", x_mean - width/2)
        print("Mean", x_mean)
        print("Exec time: {}s with parameters u={}, k={}, c={} and width={} \n"
        .format( round(time.time() - start), u, k, c, width))

    #317.4663905702453 TIME : 11s
    def test_1(self):
        start = time.time()
        width = 22
        u = 16
        k = 2
        c = 1
        x_mean = attempts_estimate(u, k, c, width)
        assert_allclose(x_mean, 322, width)
        self.print_all(x_mean, width, u, k ,c, start)

    # 3686.731214829527 TIME: 56s
    def test_2(self):
        start = time.time()
        width = 24
        u = 16
        k = 2
        c = 100
        x_mean = attempts_estimate(u, k, c, width)
        self.print_all(x_mean, width, u, k ,c, start)
        assert_allclose(x_mean, 3685, width)

    #45271.42478813559 TIME: 577s
    def test_3(self):
        start = time.time()
        width = 22
        u = 16
        k = 2
        c = 10000
        x_mean = attempts_estimate(u, k, c, width)
        self.print_all(x_mean, width, u, k ,c, start)
        assert_allclose(x_mean, 45270, width)

    # 482506.34375 TIME: 147s
    def test_4(self):
        start = time.time()
        width = 79671
        u = 20
        k = 7
        c = 1
        x_mean = attempts_estimate(u, k, c, width)
        self.print_all(x_mean, width, u, k ,c, start)
        assert_allclose(x_mean, 493981, width)

    #1068148.025 TIME: 395s
    def test_5(self):
        start = time.time()
        width = 15616
        u = 20
        k = 7
        c = 100
        x_mean = attempts_estimate(u, k, c, width)
        self.print_all(x_mean, width, u, k ,c, start)
        assert_allclose(x_mean, 1069997, width)

    #2420620.288888889 TIME: 492s
    def test_6(self):
        start = time.time()
        width = 4783
        u = 20
        k = 7
        c = 10000
        x_mean = attempts_estimate(u, k, c, width)
        self.print_all(x_mean, width, u, k ,c, start)
        assert_allclose(x_mean, 2420113, width)
        
    #449169.6482213439
    def test_7(self):
        start = time.time()
        width = 660
        u = 20
        k = 3
        c = 10000
        x_mean = attempts_estimate(u, k, c, width)
        self.print_all(x_mean, width, u, k ,c, start)
        assert_allclose(x_mean, 2420113, width)

if __name__ == '__main__':
    unittest.main()
