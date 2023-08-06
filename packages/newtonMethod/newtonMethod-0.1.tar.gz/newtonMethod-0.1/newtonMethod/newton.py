import sympy as sym
import numpy as np
import matplotlib.pyplot as plt


class Newton():

    def __init__(self, f='x**2', max_iter=1e6, eps=1e-14):
        """ Newton method class to find the solution

        Attributes:
                f (str) representing the function
                max_iter (int) representing the maximum number of iterations to find the solution
                eps (float) representing stopping criteria abs(f(x)) < epsilon
            
            Examples
            --------
            >>> f = '2*x**2 - 50'
            >>> newton = Newton(f)
            >>> newton.find_solution(1)
            x = 13.0, f(x) = 288.0, iteration #1
            x = 7.461538461538462, f(x) = 61.349112426035504, iteration #2
            x = 5.406026962727994, f(x) = 8.45025504348412, iteration #3
            x = 5.015247601944898, f(x) = 0.3054170176281019, iteration #4
            x = 5.000023178253949, f(x) = 0.00046356615344222973, iteration #5
            x = 5.000000000053723, f(x) = 1.0744685141617083e-09, iteration #6
            x = 5.0, f(x) = 0.0, iteration #7
            
            Solution found at 5.0 with 7 iterations

                """

        self.f = f  # Symbolic expression of the function
        self.max_iter = max_iter
        self.eps = eps
        x = sym.symbols('x')  # Define x as mathematical symbol
        self.x = x

    def calculate_f_value(self, x):
        """ Function to evaluate function for given x

            Args:
                x (float): x value

            Returns:
                f(x) (float): value of the function for the given x

            """

        # lambdify provides a bridge from Sympy expression to numerical libraries
        f = sym.lambdify([self.x], self.f)
        return f(x)

    def calculate_derivative(self, x):
        """ Function to find the derivative and calculate the dfdx value for given x

            Args:
                x (float): x value

            Returns:
                dfdx(x) (float): derivate of f(x) at given x
            """

        self.dfdx_expr = sym.diff(self.f, self.x)
        dfdx = sym.lambdify([self.x], self.dfdx_expr)

        return dfdx(x)

    def plot_function(self, a=-10, b=10):
        """ Function to plot the given function

            Args:
                a, b (float) [optional]: intervals

            Returns:
                None
            """
        x = np.linspace(a, b, 100)
        y = sym.lambdify([self.x], self.f)(x)

        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        ax.spines['left'].set_position('center')
        ax.spines['bottom'].set_position('zero')
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')
        ax.xaxis.set_ticks_position('bottom')
        ax.yaxis.set_ticks_position('left')
        plt.plot(x, y)
        plt.show()

    def find_solution(self, x0):
        """ Function to approximate solution of f(x)=0 by Newton's method

            Args:
                x0 (float): initial guess for a solution f(x)=0

            Returns:
                xn (float): intercept (solution) by the formula x = xn - f(xn)/dfdx(xn)

        """
        xn = x0
        iter_counter = 0
        f_value = self.calculate_f_value(xn)
        while abs(f_value) > self.eps and iter_counter < self.max_iter:
            try:
                xn = xn - float(f_value) / self.calculate_derivative(xn)
            except ZeroDivisionError:
                # Handling ZeroDivisonError - if the derivative of the initial guess is 0, increment x0
                print(
                    "Error! - derivative zero for x = {}. Incrementing by 1...".format(xn))
                xn += 1
            f_value = self.calculate_f_value(xn)
            iter_counter += 1

            print("x = {}, f(x) = {}, iteration #{}".format(
                xn, f_value, iter_counter))

        print("Solution found at {} with {} iterations".format(xn, iter_counter))
        if abs(f_value) > self.eps:
            print("Solution not found! Try changing the initial guess")
            iter_counter = -1
            xn = None
        
        return xn
