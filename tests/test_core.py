import pathlib
import subprocess
import sys

import pytest

import pytailwindcss
from pytailwindcss.exceptions import PyTailwindCssBinaryNotFound

from .fakes import FakeRelease

posix_only = pytest.mark.skipif(sys.platform == "win32", reason="the fake binary is a shell script")


@pytest.mark.network
def test_successful_run() -> None:
    """
    It installs the executable and successfully runs the CLI.
    """
    pytailwindcss.install()
    output = pytailwindcss.run("--help")
    assert isinstance(output, str)
    assert "tailwindcss" in output.lower()


@pytest.mark.network
def test_successful_run_from_custom_bin_path(tmp_path: pathlib.Path) -> None:
    """
    It installs the executable and successfully runs the CLI from a custom path.
    """
    bin_path = str(tmp_path / "custom" / "tailwindcss")
    pytailwindcss.install(bin_path=bin_path)
    output = pytailwindcss.run("--help", bin_path=bin_path)
    assert isinstance(output, str)
    assert "tailwindcss" in output.lower()


def test_unsuccessful_run() -> None:
    """
    It fails to run build command because executable is not installed.
    """
    with pytest.raises(PyTailwindCssBinaryNotFound, match="tailwindcss_install"):
        pytailwindcss.run("build")


@posix_only
def test_auto_install_with_str_bin_path(tmp_path: pathlib.Path, fake_release: FakeRelease) -> None:
    """
    It auto-installs to a bin_path given as a string, then runs the binary with the given args.
    """
    fake_release.add_binary()
    fake_release.add_valid_checksums()

    output = pytailwindcss.run("-i in.css", bin_path=str(tmp_path / "tailwindcss"), auto_install=True)

    assert output == "fake tailwindcss -i in.css"


@posix_only
def test_live_output_returns_completed_process(fake_release: FakeRelease) -> None:
    """
    With live_output it returns the CompletedProcess instead of captured output.
    """
    fake_release.add_binary()
    fake_release.add_valid_checksums()

    result = pytailwindcss.run(["--help"], live_output=True, auto_install=True)

    assert isinstance(result, subprocess.CompletedProcess)
    assert result.returncode == 0


@posix_only
def test_missing_cwd_is_not_reported_as_missing_binary(tmp_path: pathlib.Path, fake_release: FakeRelease) -> None:
    """
    A missing working directory surfaces as-is rather than as a missing binary.
    """
    fake_release.add_binary()
    fake_release.add_valid_checksums()
    pytailwindcss.install()

    with pytest.raises(FileNotFoundError):
        pytailwindcss.run("--help", cwd=tmp_path / "does-not-exist")
