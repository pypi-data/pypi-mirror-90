# Newton-Raphson Method
## Definition
The Newton-Raphson (N-R) method is one of the most widely used methods for root finding. 
It uses the idea that a continuous and differentiable function can be approximated by a straight line tangent to it.
It can be easily generalized to the problem of finding solutions of a system of non-linear equations, which is referred to as Newton's technique. 

In addition, it the technique is quadratically convergent as we approach the root. 

The most basic version starts with a 
- single-variable function *f* 
- defined for a real variable *x*,
- the function's derivative *f′*, 
- initial guess x0 for a root of *f*

If the function satisfies sufficient assumptions and the initial guess is close, then
```
x1 = x0- f(x0)/f'(x0)
 ```

## Disadvantages of Newton Method
* It is not guaranteed that Newton's method will converge if we select an x0 that is too far from the exact root. 
* We are not guaranteed convergence if our tangent line becomes parallel or almost parallel to the x-axis

# Installation

To install the package, simply run
```
pip install newtonMethod
```


