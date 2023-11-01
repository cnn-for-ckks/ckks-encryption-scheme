import numpy as np
from numpy.polynomial import polynomial
from typing import Tuple
from utils import coordinate_wise_random_rounding


class Key:
    M: int
    q0: int
    private_key: polynomial.Polynomial
    public_key: Tuple[polynomial.Polynomial, polynomial.Polynomial]
    evaluation_key: Tuple[polynomial.Polynomial, polynomial.Polynomial]

    def __init__(self, M: int, q0: int) -> None:
        assert q0 > 0, "modulo q0 must be positive"

        self.M = M
        self.q0 = q0
        self.private_key = self.generate_private_key()
        self.public_key = self.generate_public_key(self.private_key)
        self.evaluation_key = self.generate_evaluation_key(self.private_key)

    def generate_private_key(self) -> polynomial.Polynomial:
        N = self.M // 2

        # Menghasilkan private key
        coef = np.random.randint(0, self.q0, N)
        return polynomial.Polynomial(coef)

    def generate_public_key(self, private_key: polynomial.Polynomial) -> Tuple[polynomial.Polynomial, polynomial.Polynomial]:
        # Menghasilkan public key
        N = self.M // 2

        # Menghasilkan random polynomial
        coefA = np.random.randint(0, self.q0, N)
        A = polynomial.Polynomial(coefA)

        # Menghasilkan noise
        coefE = coordinate_wise_random_rounding(np.random.normal(0, 1, N))
        E = polynomial.Polynomial(coefE)

        # Menghasilkan phi
        phi = polynomial.Polynomial(
            [1 if i == 0 or i == N else 0 for i in range(N + 1)]
        )

        # Menghasilkan public key
        BRaw = (-A * private_key + E) % phi
        B = polynomial.Polynomial(
            [coef for coef in BRaw]
        )

        return B, A

    # TODO: Add big integer support
    def generate_evaluation_key(self, private_key: polynomial.Polynomial) -> Tuple[polynomial.Polynomial, polynomial.Polynomial]:
        # Menghasilkan evaluation key
        N = self.M // 2

        # Menghasilkan random polynomial
        coefA = np.random.randint(0, self.q0, N)
        A = polynomial.Polynomial(coefA)

        # Menghasilkan noise
        coefE = coordinate_wise_random_rounding(np.random.normal(0, 1, N))
        E = polynomial.Polynomial(coefE)

        # Menghasilkan phi
        phi = polynomial.Polynomial(
            [1 if i == 0 or i == N else 0 for i in range(N + 1)]
        )

        # Menghasilkan evaluation key
        BRaw = (-A * private_key + E + private_key * private_key) % phi
        B = polynomial.Polynomial(
            [coef for coef in BRaw]
        )

        return B, A
