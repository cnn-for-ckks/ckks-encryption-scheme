import numpy as np
from numpy.polynomial import polynomial
from typing import Tuple
from utils import coordinate_wise_random_rounding


class Key:
    M: int
    P: int
    q: int

    private_key: polynomial.Polynomial
    public_key: Tuple[polynomial.Polynomial, polynomial.Polynomial]
    evaluation_key: Tuple[polynomial.Polynomial, polynomial.Polynomial]

    def __init__(self, M: int, P: int, q: int) -> None:
        assert q > 0, "modulo q must be positive"

        self.M = M
        self.q = q
        self.P = P

        self.private_key = self.generate_private_key()
        self.public_key = self.generate_public_key(self.private_key)
        self.evaluation_key = self.generate_evaluation_key(
            self.private_key,
            self.P
        )

    def generate_private_key(self) -> polynomial.Polynomial:
        N = self.M // 2

        # Menghasilkan private key
        coef = np.random.randint(0, self.q, N)
        return polynomial.Polynomial(coef)

    def generate_public_key(self, private_key: polynomial.Polynomial) -> Tuple[polynomial.Polynomial, polynomial.Polynomial]:
        # Menghasilkan public key
        N = self.M // 2

        # Menghasilkan random polynomial
        coefA = np.random.randint(0, self.q, N)
        A = polynomial.Polynomial(coefA)

        # Menghasilkan noise
        coefE = coordinate_wise_random_rounding(np.random.normal(0, 1, N))
        E = polynomial.Polynomial(coefE)

        # Menghasilkan phi
        phi = polynomial.Polynomial(
            [1 if i == 0 or i == N else 0 for i in range(N + 1)]
        )

        # Menghasilkan public key
        B = (-A * private_key + E) % phi

        return B, A

    def generate_evaluation_key(self, private_key: polynomial.Polynomial, P: int) -> Tuple[polynomial.Polynomial, polynomial.Polynomial]:
        # Menghasilkan evaluation key
        N = self.M // 2

        # Menghasilkan random polynomial
        coefA = np.random.randint(0, self.q, N)
        A = polynomial.Polynomial(coefA)

        # Menghasilkan noise
        coefE = coordinate_wise_random_rounding(np.random.normal(0, 1, N))
        E = polynomial.Polynomial(coefE)

        # Menghasilkan phi
        phi = polynomial.Polynomial(
            [1 if i == 0 or i == N else 0 for i in range(N + 1)]
        )

        # Menghasilkan evaluation key
        # With big integer support
        B = (-A * private_key + E + P * private_key * private_key) % phi

        return B, A
