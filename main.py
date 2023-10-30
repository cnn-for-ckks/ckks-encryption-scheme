import numpy as np
from encoder import Encoder
from key import Key

if __name__ == "__main__":
    encoder = Encoder(M=8, scale=64.0)

    z = np.array([3 + 4j, 2 - 1j], dtype=np.complex128)
    print(f"z: {z}")

    p = encoder.encode(z)
    print(f"p: {p}")

    decoded_z = encoder.decode(p)
    print(f"decoded_z: {decoded_z}")

    key = Key(M=8, coef_size=2**6)
    print(f"private_key: {key.private_key}")
    print(f"public_key: ({key.public_key[0]}, {key.public_key[1]})")
