from typing_extensions import Annotated
from pydantic import PositiveInt
from pydantic.functional_validators import AfterValidator


def check_if_power_of_two(N: int) -> int:
    assert N & (N - 1) == 0, "N must be power of two"
    return N


ValidDimension = Annotated[PositiveInt, AfterValidator(check_if_power_of_two)]
