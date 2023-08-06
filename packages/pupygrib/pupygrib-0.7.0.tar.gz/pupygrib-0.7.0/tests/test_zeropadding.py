"""Unit tests for reading grib files with zero-padded messages."""

import io
import pkgutil

import pupygrib


def test_read_zeropadded_messages() -> None:
    data = pkgutil.get_data(__name__, "data/zeropadded.grib")
    assert data
    messages = list(pupygrib.read(io.BytesIO(data)))
    assert len(messages) == 3
