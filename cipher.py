import numpy as np
from numpy.polynomial import polynomial
from typing import Any, Tuple
from encoder import Encoder
from key import Key
from utils import check_if_power_of_two, rescale_without_level


class Cipher:
    M: int
    P: int

    encoder: Encoder
    key: Key

    def __init__(self, M: int, P: int, q0: int, delta: int) -> None:
        assert check_if_power_of_two(M), "M must be a power of two"
        assert q0 > 0, "modulo q0 must be positive"
        assert delta > 0, "delta must be positive"

        self.M = M
        self.P = P
        self.encoder = Encoder(M, delta)
        self.key = Key(M, P, q0)  # Asumsi q = q0

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

        # Do rescaling
        c_rescaled = rescale_without_level(c, self.encoder.delta)

        return c_rescaled

    def addCiphertext(self, c1: Tuple[polynomial.Polynomial, polynomial.Polynomial], c2: Tuple[polynomial.Polynomial, polynomial.Polynomial]) -> Tuple[polynomial.Polynomial, polynomial.Polynomial]:
        # Unpack ciphertexts
        B1, A1 = c1
        B2, A2 = c2

        # Add ciphertexts
        c = B1 + B2, A1 + A2

        return c

    def multCiphertext(self, c1: Tuple[polynomial.Polynomial, polynomial.Polynomial], c2: Tuple[polynomial.Polynomial, polynomial.Polynomial]) -> Tuple[polynomial.Polynomial, polynomial.Polynomial]:
        # Get evaluation key
        BEva, AEva = self.key.evaluation_key

        # Unpack ciphertexts
        B1, A1 = c1
        B2, A2 = c2

        # Get phi
        N = self.M // 2
        phi = polynomial.Polynomial(
            [1 if i == 0 or i == N else 0 for i in range(N + 1)]
        )

        # Multiply ciphertexts
        D0, D1, D2 = (B1 * B2) % phi, (B1 * A2 +
                                       A1 * B2) % phi, (A1 * A2) % phi

        # Do relinearization
        # With big integer support
        D0Lin, D1Lin = D0 + ((D2 * BEva / self.P) %
                             phi), D1 + ((D2 * AEva / self.P) % phi)
        c = D0Lin, D1Lin

        # Do rescaling
        c_rescaled = rescale_without_level(c, self.encoder.delta)

        return c_rescaled
