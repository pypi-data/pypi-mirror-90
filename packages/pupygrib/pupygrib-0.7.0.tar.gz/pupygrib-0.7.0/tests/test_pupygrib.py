"""Unit and regression tests for pupygrib's public interface."""

import io
import pkgutil
from os import path

import pytest

import pupygrib
from pupygrib import Edition1, Edition2


def open_grib(filename: str) -> io.BytesIO:
    data = pkgutil.get_data(__name__, path.join("data", filename))
    assert data
    stream = io.BytesIO(data)
    stream.name = filename
    return stream


class TestRead:

    """Unit and regression tests for the read() function."""

    def test_read_empty_file(self) -> None:
        with pytest.raises(StopIteration):
            next(pupygrib.read(io.BytesIO()))

    def test_read_not_a_grib(self) -> None:
        with pytest.raises(pupygrib.ParseError) as excinfo:
            next(pupygrib.read(io.BytesIO(b"GRUB")))
        assert "not a GRIB message" in str(excinfo.value)

    def test_read_truncated_header(self) -> None:
        with pytest.raises(pupygrib.ParseError) as excinfo:
            next(pupygrib.read(io.BytesIO(b"GRIB")))
        assert "unexpected end of file" in str(excinfo.value)

    def test_read_truncated_edition1_body(self) -> None:
        with pytest.raises(pupygrib.ParseError) as excinfo:
            next(pupygrib.read(io.BytesIO(b"GRIB\x00\x00\x09\x01")))
        assert "unexpected end of file" in str(excinfo.value)

    def test_read_truncated_edition2_body(self) -> None:
        data = b"GRIBxxx\x02\x00\x00\x00\x00\x00\x00\x00\x11"
        with pytest.raises(pupygrib.ParseError) as excinfo:
            next(pupygrib.read(io.BytesIO(data)))
        assert "unexpected end of file" in str(excinfo.value)

    def test_read_without_end_of_message_marker(self) -> None:
        data = b"GRIB\x00\x00\x0c\x017776"
        with pytest.raises(pupygrib.ParseError) as excinfo:
            next(pupygrib.read(io.BytesIO(data)))
        error_message = "end-of-message marker not found"
        assert error_message in str(excinfo.value)

    def test_read_unknown_edition(self) -> None:
        with pytest.raises(pupygrib.ParseError) as excinfo:
            next(pupygrib.read(io.BytesIO(b"GRIBxxx\x03")))
        assert "unknown edition number '3'" in str(excinfo.value)

    def test_read_edition1(self) -> None:
        with open_grib("regular_latlon_surface.grib1") as stream:
            msg = next(pupygrib.read(stream))
        assert msg.filename is not None
        assert msg.filename.endswith("regular_latlon_surface.grib1")
        assert msg.edition == 1
        assert isinstance(msg, Edition1)

    def test_read_edition2(self) -> None:
        with open_grib("regular_latlon_surface.grib2") as stream:
            msg = next(pupygrib.read(stream))
        assert msg.filename is not None
        assert msg.filename.endswith("regular_latlon_surface.grib2")
        assert msg.edition == 2
        assert isinstance(msg, Edition2)
