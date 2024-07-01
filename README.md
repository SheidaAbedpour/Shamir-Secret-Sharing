# Shamir's Secret Sharing Scheme  
The "Shamir Secret Sharing" method is a cryptographic technique developed by Adi Shamir in 1979. This technique allows a secret or sensitive information to be securely divided among multiple parties or devices. The secret is divided among `n` participants in such a way that it can be reconstructed with a minimum of `T` participants (but not less). Therefore, a polynomial of degree `T-1` needs to be chosen. The secret is the constant term (intercept) of the polynomial.

## Overview of the Implementation
1. **Generate a polynomial of degree `T-1` with random coefficients**
2. **Divide the secret among `n` participants**:
   Select `n` points from the polynomial and distribute them to the shareholders.
3. **Reconstruct the secret**:
   At least `T-1` participants are needed to reconstruct the secret. These participants collaborate to solve `T` equations with `T` unknowns to find the intercept of the polynomial, which is the secret.

## Mathematical Background
To find the intercept, the Lagrange interpolation formula is used:


$F(X) = \sum Y_i \left( \prod \frac{X - X_j}{X_i - X_j} \right)$


The secret is the intercept, $F(0)$.

## Python Implementation
The following Python code implements the Shamir Secret Sharing Scheme. The class `SSS` allows you to:
- Create shares from a given secret.
- Reconstruct the secret using the given shares.
- Plot the polynomial and the shares.

## Usage
Run `gui.py` and enter the following variables:
- **Secret (`s`)**: The secret value you want to share.
- **Number of Shares (`n`)**: The total number of shares to be created.
- **Threshold (`t`)**: The minimum number of shares required to reconstruct the secret, less than `n`.
- **Prime Modulus (`p`)**: A prime number larger than both `n` and `s`.
