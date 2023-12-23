import tempfile
from unittest.mock import MagicMock

import pytest

from locjamit import Translator


@pytest.fixture(name="tmpdir")
def fixture_tmpdir():
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture(name="translator")
def fixture_translator():
    yield MagicMock(spec_set=Translator)
