import unittest

from newton import Newton


class TestGaussianClass(unittest.TestCase):
    def setUp(self):
        self.newton = Newton(f='x**2 - 9', max_iter=1e6)

    def test_initialization(self): 
        self.assertEqual(self.newton.f, 'x**2 - 9', 'incorrect function')
        self.assertEqual(self.newton.max_iter, 1e6, 'incorrect maximum number of iterations')
    
    def test_solution1calc(self):
        self.assertEqual(round(self.newton.find_solution(1000), 2), 3.00, 'root incorrect')

    def test_solution2calc(self):
        self.assertEqual(round(self.newton.find_solution(-1000), 2), -3.00, 'root incorrect')

    def test_handlingZeroDivision(self):
        self.assertEqual(round(self.newton.find_solution(0), 2), 3.00, 'Zero Division error occured')

if __name__ == '__main__':
    unittest.main()

