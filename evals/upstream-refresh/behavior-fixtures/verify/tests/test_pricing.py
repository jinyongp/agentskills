import unittest
from pricing import total

class PriceTests(unittest.TestCase):
    def test_exact_tax(self):
        self.assertEqual(total(100, 500), 105)

    def test_half_cent(self):
        self.assertEqual(total(10, 500), 11)

    def test_zero(self):
        self.assertEqual(total(0, 500), 0)
