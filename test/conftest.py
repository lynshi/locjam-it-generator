import tempfile

import pytest


@pytest.fixture(name="tmpdir")
def fixture_tmpdir():
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir
