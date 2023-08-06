"""Test GRIB edition 1 messages."""

import pytest

from pupygrib import Edition1

gribfile = "data/regular_latlon_surface.grib1"


@pytest.mark.parametrize(
    "index,name",
    [(0, "is_"), (1, "pds"), (2, "gds"), (3, "bitmap"), (4, "bds"), (5, "end")],
)
def test_index_lookup(message: Edition1, index: int, name: str) -> None:
    assert message[index] is getattr(message, name)


@pytest.mark.parametrize("index", [-1, 6])
def test_index_error(message: Edition1, index: int) -> None:
    with pytest.raises(IndexError, match="no such section"):
        message[index]
