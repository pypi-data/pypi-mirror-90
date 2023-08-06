"""Shared fixtures for the Python test suite."""
import os

import pytest


@pytest.fixture
def rootdir() -> str:
    """The root directory of the test suite."""
    return os.path.dirname(os.path.abspath(__file__))
