import numpy as np
from numpy import polynomial
from typing import Any, Tuple


def coordinate_wise_random_rounding(coordinates: np.ndarray[Any, np.dtype[np.float64]]) -> np.ndarray[Any, np.dtype[np.int64]]:
    # Rounds coordinates randomly (Learning with Errors)

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


def rescale_without_level(c: Tuple[polynomial.Polynomial, polynomial.Polynomial], delta: int) -> Tuple[polynomial.Polynomial, polynomial.Polynomial]:
    # Unpack ciphertext
    B, A = c

    # Rescale
    B_rescaled = polynomial.Polynomial(
        coordinate_wise_random_rounding(
            B.coef / delta
        )
    )
    A_rescaled = polynomial.Polynomial(
        coordinate_wise_random_rounding(
            A.coef / delta
        )
    )

    return B_rescaled, A_rescaled

# TODO: Implement rescale_with_level


def check_if_power_of_two(number: int) -> bool:
    return number & (number - 1) == 0 and number > 2
