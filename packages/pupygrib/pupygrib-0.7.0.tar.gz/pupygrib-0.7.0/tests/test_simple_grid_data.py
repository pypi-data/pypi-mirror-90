"""Unit and regression tests for unpacking simple grid data."""

import binascii

import pytest
from pytest import approx

from pupygrib.edition1.bds import SimpleGridDataSection


def test_unpack_max() -> None:
    data = binascii.unhexlify("".join("00000c 00 7fff 7fffffff 08 ff".split()))
    section = SimpleGridDataSection(memoryview(data), 0, 12)
    with pytest.raises(OverflowError):
        section._unpack_values()


def test_unpack_max_binary_scale_factor() -> None:
    data = binascii.unhexlify("".join("00000c 00 7fff 00000000 08 ff".split()))
    section = SimpleGridDataSection(memoryview(data), 0, 12)
    with pytest.raises(OverflowError):
        section._unpack_values()


def test_unpack_small_binary_scale_factor() -> None:
    data = binascii.unhexlify("".join("00000c 00 0001 00000000 08 ff".split()))
    section = SimpleGridDataSection(memoryview(data), 0, 12)
    values = section._unpack_values()
    assert values[0] == approx(255 * 2)
