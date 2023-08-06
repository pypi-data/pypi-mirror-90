# -*- coding: utf-8 -*-
"""Fixtures for tspwplib tests"""

import os
from pathlib import Path
import pytest
from tspwplib import Alpha, Generation, GraphName

def pytest_addoption(parser):
    """Options for filepaths for pytest-tspwplib"""
    group = parser.getgroup('tspwplib')
    group.addoption(
        "--tsplib-root",
        default=os.environ.get("TSPLIB_ROOT"),
        required=False,
        type=str,
        help="Filepath to tsplib95 directory",
    )
    group.addoption(
        "--oplib-root",
        default=os.environ.get("OPLIB_ROOT"),
        required=False,
        type=str,
        help="Filepath to oplib directory",
    )


# fixtures for filepaths


@pytest.fixture(scope="function")
def tsplib_root(request) -> Path:
    """Root of tsplib95 data"""
    return Path(request.config.getoption("--tsplib-root"))


@pytest.fixture(scope="function")
def oplib_root(request) -> Path:
    """Root of the cloned OP lib"""
    return Path(request.config.getoption("--oplib-root"))

# fixtures for types


@pytest.fixture(
    scope="function",
    params=[
        Generation.gen1,
        Generation.gen2,
        Generation.gen3,
    ],
)
def generation(request) -> Generation:
    """Loop through valid generations"""
    # NOTE generation 4 has different alpha values
    return request.param


@pytest.fixture(scope="function", params=[Alpha.fifty])
def alpha(request) -> Alpha:
    """Alpha values"""
    return request.param


@pytest.fixture(
    scope="function",
    params=[
        GraphName.eil76,
        GraphName.st70,
        GraphName.rat195,
    ],
)
def graph_name(request) -> GraphName:
    """Loop through valid instance names"""
    return request.param


# fixtures for complete graphs


@pytest.fixture(
    scope="function",
    params=[
        0.0,
        0.1,
        0.5,
        0.9,
        1.0,
    ],
)
def edge_removal_probability(request) -> float:
    """Different valid values for probability of removing an edge"""
    return request.param
