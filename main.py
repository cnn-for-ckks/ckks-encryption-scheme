import numpy as np
from numpy.polynomial import Polynomial
from typing import Any


# Rounds coordinates randonmly (Learning with Errors)
def coordinate_wise_random_rounding(coordinates: np.ndarray[Any, np.dtype[np.float64]]) -> np.ndarray[Any, np.dtype[np.int64]]:
    r = np.array(coordinates - np.floor(coordinates), dtype=np.float64)
    f = np.array(
        [
            np.random.choice([c, c - 1], 1, p=[1 - c, c])
            for c in r
        ],
        dtype=np.float64
    ).reshape(-1)

    float_rounded_coordinates = np.array(coordinates - f, dtype=np.float64)
    int_coordinates = [
        int(np.real(coeff))
        for coeff in float_rounded_coordinates
    ]

    return np.array(int_coordinates, dtype=np.int64)


class Encoder:
    xi: np.complex128
    M: int
    sigma_R_basis: np.ndarray[Any, np.dtype[np.complex128]]
    scale: float

    def __init__(self, M: int, scale: float) -> None:
        # Atribut xi merupakan M-th root of unity yang akan digunakan sebagai basis perhitungan
        self.xi = np.exp(2 * np.pi * 1j / M)
        self.M = M
        self.sigma_R_basis = self.vandermonde().transpose()
        self.scale = scale

    def vandermonde(self) -> np.ndarray[Any, np.dtype[np.complex128]]:
        # Menghasilkan matriks Vandermonde
        N = self.M // 2
        matrix = np.array([], dtype=np.complex128).reshape(0, N)

        for i in range(N):
            root = self.xi ** (2 * i + 1)
            row = np.array([], dtype=np.complex128)

            for j in range(N):
                row = np.append(row, root ** j)

            matrix = np.vstack([matrix, row])

        return matrix

    def sigma_inverse(self, b: np.ndarray[Any, np.dtype[np.complex128]]) -> Polynomial:
        # Melakukan encoding dari vector ke polynomial menggunakan M-th root of unity
        A = self.vandermonde()

        # Mencari solusi dari Ax = b
        coefficients = np.linalg.solve(A, b)

        # Mengembalikan polynomial dengan koefisien yang telah ditemukan
        return Polynomial(coefficients)

    def sigma(self, p: Polynomial) -> np.ndarray[Any, np.dtype[np.complex128]]:
        # Melakukan decoding dari polynomial ke vector dengan mengaplikasikan ke M-th root of unity
        outputs = np.array([], dtype=np.complex128)
        N = self.M // 2

        # Mengaplikasikan polynomial ke M-th root of unity
        for i in range(N):
            root = self.xi ** (2 * i + 1)
            output = np.complex128(p(root))

            # Imajiner bernilai mendekati 0 (masih compliance terhadap np.allclose)
            outputs = np.append(outputs, output)

        return outputs

    def pi(self, z: np.ndarray[Any, np.dtype[np.complex128]]) -> np.ndarray[Any, np.dtype[np.complex128]]:
        # Melakukan proyeksi dari vector H ke C^{N / 2}
        N = self.M // 4

        return z[:N]

    def pi_inverse(self, z: np.ndarray[Any, np.dtype[np.complex128]]) -> np.ndarray[Any, np.dtype[np.complex128]]:
        # Melakukan proyeksi dari vector C^{N / 2} ke H
        z_conjugate = np.conjugate(z[::-1])

        return np.concatenate([z, z_conjugate])

    def compute_basis_coordinates(self, z: np.ndarray[Any, np.dtype[np.complex128]]) -> np.ndarray[Any, np.dtype[np.float64]]:
        # Menghitung koordinat basis dari z
        output = np.array(
            [
                np.real(np.vdot(z, b) / np.vdot(b, b))
                for b in self.sigma_R_basis
            ],
            dtype=np.float64
        )

        return output

    def sigma_R_discretization(self, z: np.ndarray[Any, np.dtype[np.complex128]]) -> np.ndarray[Any, np.dtype[np.complex128]]:
        # Melakukan diskretisasi dari z
        coordinates = self.compute_basis_coordinates(z)
        rounded_coordinates = coordinate_wise_random_rounding(coordinates)

        return np.matmul(self.sigma_R_basis.transpose(), rounded_coordinates)

    def encode(self, z: np.ndarray[Any, np.dtype[np.complex128]]) -> Polynomial:
        # Melakukan encoding dari vector ke polynomial
        pi_z = self.pi_inverse(z)
        scaled_pi_z = np.array(self.scale * pi_z, dtype=np.complex128)
        sigma_R_discretization = self.sigma_R_discretization(scaled_pi_z)
        raw_p = self.sigma_inverse(sigma_R_discretization)

        # Round coefficient to the nearest integer
        coefficients = np.round(np.real(raw_p.coef), 0).astype(np.int64)
        p = Polynomial(coefficients)

        return p

    def decode(self, p: Polynomial) -> np.ndarray[Any, np.dtype[np.complex128]]:
        # Melakukan decoding dari polynomial ke vector
        coefficients = np.array(p.coef / self.scale, dtype=np.complex128)
        rescaled_p = Polynomial(coefficients)
        z = self.sigma(rescaled_p)
        pi_z = self.pi(z)

        return pi_z


if __name__ == "__main__":
    encoder = Encoder(8, 64)

    z = np.array([3 + 4j, 2 - 1j], dtype=np.complex128)
    print(z)

    p = encoder.encode(z)
    print(p)

    decoded_z = encoder.decode(p)
    print(decoded_z)
