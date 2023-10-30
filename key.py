from ast import Tuple
import numpy as np
from numpy.polynomial import polynomial
from typing import Tuple


class Key:
    M: int
    coef_size: int
    private_key: polynomial.Polynomial
    public_key: Tuple[polynomial.Polynomial, polynomial.Polynomial]

    def __init__(self, M: int, coef_size: int) -> None:
        self.M = M
        self.coef_size = coef_size
        self.private_key = self.generate_private_key()
        self.public_key = self.generate_public_key(self.private_key)

    def generate_private_key(self) -> polynomial.Polynomial:
        N = self.M // 2

        # Menghasilkan private key
        coef = np.random.randint(-self.coef_size, self.coef_size, N)
        return polynomial.Polynomial(coef)

    def generate_public_key(self, private_key: polynomial.Polynomial) -> Tuple[polynomial.Polynomial, polynomial.Polynomial]:
        # Menghasilkan public key
        N = self.M // 2

        # Menghasilkan public key
        coefA = np.random.randint(-self.coef_size, self.coef_size, N)
        A = polynomial.Polynomial(coefA)

        # Menghasilkan noise
        coefE = np.round(np.random.normal(-self.coef_size, self.coef_size, N))
        E = polynomial.Polynomial(coefE)

        # Menghasilkan public key
        phi = polynomial.Polynomial(
            [1 if i == 0 or i == N else 0 for i in range(N + 1)]
        )
        B = (-A * private_key + E) % phi

        return B, A
