import numpy as np
import sympy as sp
import random
from sympy.ntheory.generate import nextprime
from sympy import isprime


class SSS:
    def __init__(self, s, n, t, p=None):
        self.s = s
        self.n = n
        self.t = t
        self.p = p if p else nextprime(s)

        if t > n:
            raise ValueError("Threshold can't be greater than Shares")
        if not isprime(p):
            raise ValueError("p must be prime")
        self.coeffs = [self.s] + [random.randint(1, self.p-1) for _ in range(t-1)]


if __name__ == "__main__":
    print("SSS")
    SSS(50, 4, 3, 3)
