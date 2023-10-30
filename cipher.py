import numpy as np
from numpy.polynomial import polynomial
from typing import Any, Tuple
from pydantic import PositiveInt

from defined_types import ValidDimension
from encoder import Encoder
from key import Key


class Cipher:
    M: ValidDimension
    encoder: Encoder
    key: Key

    def __init__(self, M: ValidDimension, scale: PositiveInt, coef_size: PositiveInt) -> None:
        self.M = M
        self.encoder = Encoder(M, scale)
        self.key = Key(M, coef_size)

    def encrypt(self, z: np.ndarray[Any, np.dtype[np.complex128]]) -> Tuple[polynomial.Polynomial, polynomial.Polynomial]:
        # Get public key
        B, A = self.key.public_key

        # Encode z
        p = self.encoder.encode(z)

        # Encrypt p
        c = p + B, A

        return c

    def decrypt(self, c: Tuple[polynomial.Polynomial, polynomial.Polynomial]) -> np.ndarray[Any, np.dtype[np.complex128]]:
        # Get private key
        sk = self.key.private_key

        # Get phi
        N = self.M // 2
        phi = polynomial.Polynomial(
            [1 if i == 0 or i == N else 0 for i in range(N + 1)]
        )

        # Decrypt c
        B, A = c
        p = (B + sk * A) % phi

        # Decode p
        z = self.encoder.decode(p)

        return z
