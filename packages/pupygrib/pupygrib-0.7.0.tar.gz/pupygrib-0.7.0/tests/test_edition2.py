"""Test GRIB edition 2 messages."""

import pytest

from pupygrib import Edition2

gribfile = "data/regular_latlon_surface.grib2"


@pytest.mark.parametrize(
    "index,name",
    [
        (0, "is_"),
        (1, "ids"),
        (2, "loc"),
        (3, "gds"),
        (4, "pds"),
        (5, "drs"),
        (6, "bitmap"),
        (7, "data"),
        (8, "end"),
    ],
)
def test_index_lookup(message: Edition2, index: int, name: str) -> None:
    assert message[index] is getattr(message, name)


@pytest.mark.parametrize("index", [-1, 9])
def test_index_error(message: Edition2, index: int) -> None:
    with pytest.raises(IndexError, match="no such section"):
        message[index]
