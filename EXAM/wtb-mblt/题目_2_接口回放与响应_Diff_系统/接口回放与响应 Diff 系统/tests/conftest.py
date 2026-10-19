import os
import uuid
from pathlib import Path

import pytest
from hypothesis import settings
from hypothesis.database import DirectoryBasedExampleDatabase

PROJECT = Path(__file__).resolve().parents[1]
TEST_RUNTIME = PROJECT / ".cache" / "test-runs" / uuid.uuid4().hex
TEST_RUNTIME.mkdir(parents=True, exist_ok=True)
for name in ("TMP", "TEMP", "TMPDIR"):
    os.environ[name] = str(TEST_RUNTIME)
os.environ["PYTHONUTF8"] = "1"
settings.register_profile("project", max_examples=200, deadline=None, database=DirectoryBasedExampleDatabase(PROJECT / ".cache" / "hypothesis"))
settings.load_profile("project")


def pytest_configure(config):
    if config.option.basetemp is None:
        config.option.basetemp = str(TEST_RUNTIME / "pytest")


@pytest.fixture
def project():
    return PROJECT
