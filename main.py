import numpy as np
from cipher import Cipher

if __name__ == "__main__":
    np.random.seed(42)

    cipher = Cipher(M=8, integer_scale=2**8, decimal_scale=2**8)

    BPublic, APublic = cipher.key.public_key
    print(f"public key: ({BPublic}, {APublic})")

    private_key = cipher.key.private_key
    print(f"private key: {private_key}")

    # Border
    print()

    p1 = np.array([3 + 4j, 2 - 1j], dtype=np.complex128)
    print(f"p1: {p1}")

    p2 = np.array([4 + 3j, 1 - 2j], dtype=np.complex128)
    print(f"p2: {p2}")

    pOperation = p1 * p2
    print(f"pOperation: {pOperation}")

    # Border
    print()

    c1 = cipher.encrypt(p1)
    B1, A1 = c1
    print(f"c1: ({B1}, {A1})")

    c2 = cipher.encrypt(p2)
    B2, A2 = c2
    print(f"c2: ({B2}, {A2})")

    cOperation = cipher.addCiphertext(c1, c2)
    BOperation, AOperation = cOperation
    print(f"cOperation: ({BOperation}, {AOperation})")

    # Border
    print()

    p1_deciphered = cipher.decrypt(c1)
    print(f"p1 deciphered: {p1_deciphered}")

    p2_deciphered = cipher.decrypt(c2)
    print(f"p2 deciphered: {p2_deciphered}")

    pOperation_deciphered = cipher.decrypt(cOperation)
    print(f"pOperation deciphered: {pOperation_deciphered}")
