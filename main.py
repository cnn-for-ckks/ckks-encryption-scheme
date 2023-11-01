import numpy as np
from cipher import Cipher

if __name__ == "__main__":
    np.random.seed(42)

    cipher = Cipher(M=8, q0=2**16, delta=2**24)

    p1 = np.array([3 + 4j, 2 - 1j], dtype=np.complex128)
    print(f"p1: {p1}")

    p2 = np.array([4 + 3j, 1 - 2j], dtype=np.complex128)
    print(f"p2: {p2}")

    pOperation = p1 * p2
    print(f"p1 * p2: {pOperation}")

    # Border
    print()

    c1 = cipher.encrypt(p1)
    print(f"enc(p1): ({c1[0]}, {c1[1]})")

    c2 = cipher.encrypt(p2)
    print(f"enc(p2): ({c2[0]}, {c2[1]})")

    cOperation = cipher.multCiphertext(c1, c2)
    print(f"enc(p1) * enc(p2): ({cOperation[0]}, {cOperation[1]})")

    # Border
    print()

    p1_deciphered = cipher.decrypt(c1)
    print(f"dec(enc(p1)): {p1_deciphered}")

    p2_deciphered = cipher.decrypt(c2)
    print(f"dec(enc(p2)): {p2_deciphered}")

    pOperation_deciphered = cipher.decrypt(cOperation)
    print(f"dec(enc(p1) * enc(p2)): {pOperation_deciphered}")
