import unittest
import numpy as np
from utils import black_scholes_call, black_scholes_put, generate_option_matrix

class TestBlackScholes(unittest.TestCase):
    def test_black_scholes_call(self):
        result = black_scholes_call(100, 100, 1, 0.05, 0.2)
        self.assertAlmostEqual(result, 10.45, places=1)

    def test_black_scholes_put(self):
        result = black_scholes_put(100, 100, 1, 0.05, 0.2)
        self.assertAlmostEqual(result, 5.57, places=1)

    def test_generate_option_matrix_shape(self):
        matrix, sigmas, strikes = generate_option_matrix()
        self.assertEqual(matrix.shape, (10, 10))
        self.assertEqual(len(sigmas), 10)
        self.assertEqual(len(strikes), 10)

if __name__ == '__main__':
    unittest.main()