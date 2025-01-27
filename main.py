import numpy as np
import sympy as sp
import random
from sympy.ntheory.generate import nextprime
from sympy import isprime, mod_inverse
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')


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
        self.shares = self._generate_shares()

    def _generate_shares(self):
        shares = []
        for i in range(1, self.n+1):
            poly_i = sum([coff * (i ** power) for power, coff in enumerate(self.coeffs)]) % self.p
            shares.append((i, poly_i))
        return shares

    def get_shares(self):
        return self.shares, self.coeffs, self.p

    def reconstruct_secret(self, shares):
        if len(shares) < self.t:
            raise ValueError("Insufficient number of shares to reconstruct the secret.")
        secret = self._lagrange_interpolation(0, shares)
        return secret

    def _lagrange_interpolation(self, x, shares):
        def L(x, i):
            numerator = 1
            denominator = 1
            for j in range(self.t):
                if j != i:
                    numerator = (numerator * (x - shares[j][0])) % self.p
                    denominator = (denominator * (shares[i][0] - shares[j][0])) % self.p
            return (numerator * mod_inverse(denominator, self.p)) % self.p

        return sum([shares[i][1] * L(x, i) % self.p for i in range(self.t)]) % self.p

    def plot_polynomial(self, selected_shares):
        x_vals = list(range(self.p))
        y_vals = [sum([coeff * (x ** i) for i, coeff in enumerate(self.coeffs)]) % self.p for x in x_vals]

        plt.figure(figsize=(10, 6))
        plt.plot(x_vals, y_vals, label='Polynomial', color='blue')

        shares_x = [share[0] for share in self.shares]
        shares_y = [share[1] for share in self.shares]
        plt.scatter(shares_x, shares_y, label='All Shares', color='red')

        selected_x = [share[0] for share in selected_shares]
        selected_y = [share[1] for share in selected_shares]
        plt.scatter(selected_x, selected_y, label=f'{len(selected_shares)} Shares for Reconstruction', color='green')

        plt.xlabel('x')
        plt.ylabel('y')
        plt.title("Shamir's Secret Sharing Polynomial")
        plt.legend()
        plt.grid(True)

        plot_filename = 'shamir_polynomial_plot.png'
        plt.savefig(plot_filename)
        plt.close()


if __name__ == "__main__":

    secret = 6
    num_shares = 5
    threshold = 3
    p_mode = 13

    sss = SSS(secret, num_shares, threshold, p_mode)
    shares, coeffs, p_mode = sss.get_shares()
    print(f'Generated shares: {shares} \n')

    # Check if reconstructing with fewer shares than 't' raises an error
    try:
        invalid_shares = shares[:threshold-1]
        sss.reconstruct_secret(invalid_shares)
    except ValueError as e:
        print(f'Error: {e} \n')

    # Check if reconstructing with correct number of shares works
    try:
        valid_shares = shares[:threshold]
        reconstructed_secret = sss.reconstruct_secret(valid_shares)
        print("Reconstructed secret with valid shares:", reconstructed_secret)
    except ValueError as e:
        print(f'Error: {e} \n')

    # Check if reconstructing with more shares than 't' still works
    try:
        more_shares = shares[:num_shares]
        reconstructed_secret = sss.reconstruct_secret(more_shares)
        print("Reconstructed secret with more shares:", reconstructed_secret)
    except ValueError as e:
        print(f'Error: {e} \n')

    sss.plot_polynomial(shares[:threshold])

