import pathlib

import pytest

from pytailwindcss import installation
from pytailwindcss.utils import BIN_DIR_ENV_VAR

from .fakes import FAKE_TARGET, FakeRelease


@pytest.fixture(autouse=True)
def bin_dir(tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch) -> pathlib.Path:
    """
    Every test installs binaries into its own temporary directory, never into the package.
    """
    path = tmp_path / "bin"
    monkeypatch.setenv(BIN_DIR_ENV_VAR, str(path))
    return path


@pytest.fixture
def fake_release(monkeypatch: pytest.MonkeyPatch) -> FakeRelease:
    release = FakeRelease()
    monkeypatch.setattr(installation, "open_url", release.open_url)
    monkeypatch.setattr(installation, "detect_target", lambda: FAKE_TARGET)
    return release
