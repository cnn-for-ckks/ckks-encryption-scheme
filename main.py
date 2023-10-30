import numpy as np
from cipher import Cipher

if __name__ == "__main__":
    np.random.seed(42)

    cipher = Cipher(M=8, scale=2**8, coef_size=2**8)

    plaintext = np.array([3 + 4j, 2 - 1j], dtype=np.complex128)
    print(f"plaintext: {plaintext}")

    ciphertext = cipher.encrypt(plaintext)
    print(f"ciphertext: ({ciphertext[0]}, {ciphertext[1]})")

    deciphered = cipher.decrypt(ciphertext)
    print(f"deciphered: {deciphered}")
