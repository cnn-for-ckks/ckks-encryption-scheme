import numpy as np
from numpy.polynomial import polynomial
from typing import Any
from pydantic import PositiveInt

from defined_types import ValidDimension
from utils import coordinate_wise_random_rounding


class Encoder:
    M: ValidDimension
    scale: PositiveInt
    xi: np.complex128
    sigma_R_basis: np.ndarray[Any, np.dtype[np.complex128]]

    def __init__(self, M: ValidDimension, scale: PositiveInt) -> None:
        self.M = M
        self.scale = scale

        # Atribut xi merupakan M-th root of unity yang akan digunakan sebagai basis perhitungan
        self.xi = np.exp(2 * np.pi * 1j / M)

        # Atribut sigma_R_basis merupakan matriks basis dari sigma_R
        self.sigma_R_basis = self.vandermonde().transpose()

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

    def sigma_inverse(self, b: np.ndarray[Any, np.dtype[np.complex128]]) -> polynomial.Polynomial:
        # Melakukan encoding dari vector ke polynomial menggunakan M-th root of unity
        A = self.vandermonde()

        # Mencari solusi dari Ax = b
        coefficients = np.linalg.solve(A, b)

        # Mengembalikan polynomial dengan koefisien yang telah ditemukan
        return polynomial.Polynomial(coefficients)

    def sigma(self, p: polynomial.Polynomial) -> np.ndarray[Any, np.dtype[np.complex128]]:
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
        N_per_2 = self.M // 4

        return z[:N_per_2]

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

    def encode(self, z: np.ndarray[Any, np.dtype[np.complex128]]) -> polynomial.Polynomial:
        # Melakukan encoding dari vector ke polynomial
        pi_z = self.pi_inverse(z)
        scaled_pi_z = np.array(self.scale * pi_z, dtype=np.complex128)
        sigma_R_discretization = self.sigma_R_discretization(scaled_pi_z)
        raw_p = self.sigma_inverse(sigma_R_discretization)

        # Round coefficient to the nearest integer
        coefficients = np.round(np.real(raw_p.coef), 0).astype(np.int64)
        p = polynomial.Polynomial(coefficients)

        return p

    def decode(self, p: polynomial.Polynomial) -> np.ndarray[Any, np.dtype[np.complex128]]:
        # Melakukan decoding dari polynomial ke vector
        coefficients = np.array(p.coef / self.scale, dtype=np.complex128)
        rescaled_p = polynomial.Polynomial(coefficients)
        z = self.sigma(rescaled_p)
        pi_z = self.pi(z)

        return pi_z
