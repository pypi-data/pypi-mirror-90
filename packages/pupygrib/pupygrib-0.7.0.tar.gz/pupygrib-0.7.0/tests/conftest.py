"""Test fixtures for pupygrib."""

import io
import itertools
import pkgutil
from operator import itemgetter
from os import path
from typing import Any, Iterable, Iterator, Tuple

import numpy as np
import pytest
from pytest import FixtureRequest

import pupygrib
from pupygrib import Message


@pytest.fixture(scope="module")
def message(request: FixtureRequest) -> Message:
    data = pkgutil.get_data(__name__, request.module.gribfile)
    assert data
    return next(pupygrib.read(io.BytesIO(data)))


@pytest.fixture(scope="class")
def section(request: FixtureRequest, message: Message) -> Any:
    return getattr(message, request.cls.section_name)


Grid = Tuple[np.ndarray, np.ndarray, np.ndarray]


@pytest.fixture(scope="module")
def target_field(request: FixtureRequest) -> Grid:
    def _iterrows(lines: Iterable[str]) -> Iterator[Iterator[Tuple[Any, ...]]]:
        rows = (line.split() for line in lines)
        for lat, subrows in itertools.groupby(rows, itemgetter(0)):
            yield zip(*(map(float, row) for row in subrows))

    datafile = path.extsep.join([request.module.gribfile, "values"])
    data = pkgutil.get_data(__name__, datafile)
    assert data
    stream = iter(data.decode("ascii").splitlines())
    assert next(stream).strip() == "Latitude, Longitude, Value"
    lats, lons, values = map(np.vstack, zip(*_iterrows(stream)))
    return lons, lats, values


@pytest.fixture(scope="module")
def target_longitudes(target_field: Grid) -> np.ndarray:
    return target_field[0]


@pytest.fixture(scope="module")
def target_latitudes(target_field: Grid) -> np.ndarray:
    return target_field[1]


@pytest.fixture(scope="module")
def target_values(target_field: Grid) -> np.ndarray:
    return target_field[2]
