import numpy as np
from numpy.polynomial import polynomial
from typing import Any, Tuple
from encoder import Encoder
from key import Key
from utils import check_if_power_of_two


class Cipher:
    M: int
    integer_scale: int
    decimal_scale: int
    encoder: Encoder
    key: Key

    def __init__(self, M: int, integer_scale: int, decimal_scale: int) -> None:
        assert check_if_power_of_two(M), "M must be a power of two"
        assert decimal_scale > 0, "scale must be positive"

        self.M = M
        self.integer_scale = integer_scale
        self.decimal_scale = decimal_scale
        self.encoder = Encoder(M, decimal_scale)
        self.key = Key(M, integer_scale)

    def encrypt(self, z: np.ndarray[Any, np.dtype[np.complex128]]) -> Tuple[polynomial.Polynomial, polynomial.Polynomial]:
        # Get public key
        B, A = self.key.public_key

        # Encode z
        p = self.encoder.encode(z)

        # Encrypt p
        c = B + p, A

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

    def addPlaintext(self, c: Tuple[polynomial.Polynomial, polynomial.Polynomial], z: np.ndarray[Any, np.dtype[np.complex128]]) -> Tuple[polynomial.Polynomial, polynomial.Polynomial]:
        # Unpack ciphertext
        B, A = c

        # Encode z
        p = self.encoder.encode(z)

        # Add p to ciphertext
        c = B + p, A

        return c

    def multPlaintext(self, c: Tuple[polynomial.Polynomial, polynomial.Polynomial], z: np.ndarray[Any, np.dtype[np.complex128]]) -> Tuple[polynomial.Polynomial, polynomial.Polynomial]:
        # Unpack ciphertext
        B, A = c

        # Encode z
        p = self.encoder.encode(z)

        # Get phi
        N = self.M // 2
        phi = polynomial.Polynomial(
            [1 if i == 0 or i == N else 0 for i in range(N + 1)]
        )

        # Multiply p to ciphertext
        c = (B * p) % phi, (A * p) % phi

        # TODO: Do rescaling

        return c

    def addCiphertext(self, c1: Tuple[polynomial.Polynomial, polynomial.Polynomial], c2: Tuple[polynomial.Polynomial, polynomial.Polynomial]) -> Tuple[polynomial.Polynomial, polynomial.Polynomial]:
        # Unpack ciphertexts
        B1, A1 = c1
        B2, A2 = c2

        # Add ciphertexts
        c = B1 + B2, A1 + A2

        return c

    def multCiphertext(self, c1: Tuple[polynomial.Polynomial, polynomial.Polynomial], c2: Tuple[polynomial.Polynomial, polynomial.Polynomial]) -> Tuple[polynomial.Polynomial, polynomial.Polynomial, polynomial.Polynomial]:
        # Unpack ciphertexts
        B1, A1 = c1
        B2, A2 = c2

        # Get phi
        N = self.M // 2
        phi = polynomial.Polynomial(
            [1 if i == 0 or i == N else 0 for i in range(N + 1)]
        )

        # Multiply ciphertexts
        c = (B1 * B2) % phi, (B1 * A2 + A1 * B2) % phi, (A1 * A2) % phi

        # TODO: Do relinearization

        # TODO: Do rescaling

        return c
