import numpy as np
from encoder import Encoder

if __name__ == "__main__":
    encoder = Encoder(8, 64)

    z = np.array([3 + 4j, 2 - 1j], dtype=np.complex128)
    print(z)

    p = encoder.encode(z)
    print(p)

    decoded_z = encoder.decode(p)
    print(decoded_z)
