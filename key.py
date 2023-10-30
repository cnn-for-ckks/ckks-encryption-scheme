import numpy as np
from numpy.polynomial import polynomial
from typing import Tuple
from utils import check_if_power_of_two, coordinate_wise_random_rounding


class Key:
    M: int
    coef_size: int
    private_key: polynomial.Polynomial
    public_key: Tuple[polynomial.Polynomial, polynomial.Polynomial]

    def __init__(self, M: int, coef_size: int) -> None:
        assert check_if_power_of_two(M), "M must be a power of two"
        assert coef_size > 0, "coef_size must be positive"

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
        coefE = coordinate_wise_random_rounding(np.random.normal(0, 1, N))
        E = polynomial.Polynomial(coefE)

        # Menghasilkan public key
        phi = polynomial.Polynomial(
            [1 if i == 0 or i == N else 0 for i in range(N + 1)]
        )
        B = (-A * private_key + E) % phi

        return B, A
