import http.client
import logging
import os
import pathlib
import ssl
import subprocess
import sys
import sysconfig
from urllib.error import URLError

import pytest

import pytailwindcss
from pytailwindcss import installation
from pytailwindcss.exceptions import (
    PyTailwindCssChecksumMismatch,
    PyTailwindCssException,
    PyTailwindCssVersionNotFound,
)
from pytailwindcss.installation import detect_target, format_target, is_musl
from pytailwindcss.utils import BIN_DIR_ENV_VAR, get_bin_path

from .fakes import FAKE_BINARY, FakeRelease


@pytest.mark.network
def test_install() -> None:
    """
    It installs the 'latest' binary, verified against the release checksums, at the expected path.
    """
    installed = pytailwindcss.install()
    assert installed == get_bin_path()
    assert installed.is_file()


@pytest.mark.network
@pytest.mark.skipif(is_musl(), reason="Tailwind CSS v3 has no musl builds")
def test_version_install(caplog: pytest.LogCaptureFixture) -> None:
    """
    It installs a v3 binary, which predates published checksums, and warns about skipping verification.
    """
    pytailwindcss.install(version="v3.0.5")
    output = pytailwindcss.run(version="v3.0.5")
    assert isinstance(output, str)
    assert "3.0.5" in output
    assert "skipping checksum verification" in caplog.text


@pytest.mark.network
def test_cli_install_command_with_version() -> None:
    """
    The 'tailwindcss_install' command installs the version set in TAILWINDCSS_VERSION.
    """
    test_version = "v4.0.5"
    env = {**os.environ, "TAILWINDCSS_VERSION": test_version}
    result = subprocess.run(["tailwindcss_install"], env=env, capture_output=True, text=True)

    assert result.returncode == 0, f"CLI command failed with: {result.stderr}"
    assert get_bin_path(test_version).is_file()
    output = pytailwindcss.run(version=test_version)
    assert isinstance(output, str)
    assert "4.0.5" in output


@pytest.mark.network
def test_cli_install_command_without_version() -> None:
    """
    The 'tailwindcss_install' command installs 'latest' when TAILWINDCSS_VERSION isn't set.
    """
    env = {key: value for key, value in os.environ.items() if key != "TAILWINDCSS_VERSION"}
    result = subprocess.run(["tailwindcss_install"], env=env, capture_output=True, text=True)

    assert result.returncode == 0, f"CLI command failed with: {result.stderr}"
    assert get_bin_path("latest").is_file()


def test_install_verifies_checksum(fake_release: FakeRelease) -> None:
    fake_release.add_binary()
    fake_release.add_valid_checksums()

    installed = pytailwindcss.install()

    assert installed.read_bytes() == FAKE_BINARY
    if sys.platform != "win32":
        assert installed.stat().st_mode & 0o777 == 0o755


def test_install_rejects_checksum_mismatch(fake_release: FakeRelease) -> None:
    fake_release.add_binary(b"tampered")
    fake_release.add_valid_checksums()

    with pytest.raises(PyTailwindCssChecksumMismatch, match="not installed"):
        pytailwindcss.install()
    assert not get_bin_path().parent.exists() or not any(get_bin_path().parent.iterdir())


def test_install_rejects_checksums_without_entry(fake_release: FakeRelease) -> None:
    fake_release.add_binary()
    fake_release.add_checksums(f"{'0' * 64}  ./tailwindcss-macos-x64\n".encode())

    with pytest.raises(PyTailwindCssChecksumMismatch, match="no entry"):
        pytailwindcss.install()
    assert not get_bin_path().exists()


def test_install_without_published_checksums_warns(
    fake_release: FakeRelease, caplog: pytest.LogCaptureFixture
) -> None:
    fake_release.add_binary()

    with caplog.at_level(logging.WARNING):
        installed = pytailwindcss.install()

    assert installed.read_bytes() == FAKE_BINARY
    assert "skipping checksum verification" in caplog.text


def test_failed_install_keeps_existing_binary(fake_release: FakeRelease) -> None:
    bin_path = get_bin_path()
    bin_path.parent.mkdir(parents=True)
    bin_path.write_bytes(b"previous binary")
    fake_release.add_binary(b"tampered")
    fake_release.add_valid_checksums()

    with pytest.raises(PyTailwindCssChecksumMismatch):
        pytailwindcss.install()

    assert bin_path.read_bytes() == b"previous binary"
    assert list(bin_path.parent.iterdir()) == [bin_path], "temporary download is cleaned up"


def test_install_unknown_version(fake_release: FakeRelease) -> None:
    with pytest.raises(PyTailwindCssVersionNotFound, match="tailwindlabs/tailwindcss/releases"):
        pytailwindcss.install()


@pytest.mark.parametrize(
    ("error", "message"),
    [
        (installation.HTTPError("u", 503, "Service Unavailable", None, None), "HTTP 503 Service Unavailable"),  # type: ignore[arg-type]
        (URLError("Name or service not known"), "Name or service not known"),
        (TimeoutError("timed out"), "timed out"),
        (ConnectionResetError("Connection reset by peer"), "Connection reset by peer"),
        (http.client.IncompleteRead(b""), "IncompleteRead"),
        (ssl.SSLError("bad record mac"), "bad record mac"),
    ],
)
def test_install_network_errors_are_readable(fake_release: FakeRelease, error: Exception, message: str) -> None:
    fake_release.fail_binary(error)

    with pytest.raises(PyTailwindCssException, match=message) as exc_info:
        pytailwindcss.install()
    assert not isinstance(exc_info.value, PyTailwindCssVersionNotFound)


def test_install_into_unwritable_dir(tmp_path: pathlib.Path, fake_release: FakeRelease) -> None:
    # A file where the directory should be fails on every OS, even when running as root.
    blocker = tmp_path / "blocker"
    blocker.write_text("")

    with pytest.raises(PyTailwindCssException, match=BIN_DIR_ENV_VAR):
        pytailwindcss.install(bin_path=blocker / "tailwindcss")


def test_install_reports_replace_failure(fake_release: FakeRelease, monkeypatch: pytest.MonkeyPatch) -> None:
    """
    A binary that can't be swapped in (e.g. still running on Windows) gives a readable error and no leftovers.
    """
    fake_release.add_binary()
    fake_release.add_valid_checksums()

    def locked_replace(src: object, dst: object) -> None:
        raise PermissionError(13, "The process cannot access the file")

    monkeypatch.setattr(installation.os, "replace", locked_replace)

    with pytest.raises(PyTailwindCssException, match="Can't write the Tailwind CSS binary"):
        pytailwindcss.install()
    assert list(get_bin_path().parent.iterdir()) == []


def test_download_progress_goes_to_stderr(fake_release: FakeRelease, capsys: pytest.CaptureFixture[str]) -> None:
    fake_release.add_binary()
    fake_release.add_valid_checksums()

    pytailwindcss.install()

    captured = capsys.readouterr()
    assert captured.out == ""
    assert "Downloading 'tailwindcss-linux-x64'" in captured.err


@pytest.mark.parametrize(
    ("os_name", "arch", "musl", "target"),
    [
        ("win32", "x86_64", False, "windows-x64.exe"),
        ("Windows", "AMD64", False, "windows-x64.exe"),
        ("darwin", "x86_64", False, "macos-x64"),
        ("Darwin", "arm64", False, "macos-arm64"),
        ("darwin", "ARM64", True, "macos-arm64"),
        ("linux", "x86_64", False, "linux-x64"),
        ("Linux", "AMD64", False, "linux-x64"),
        ("linux", "aarch64", False, "linux-arm64"),
        ("linux", "X86_64", True, "linux-x64-musl"),
        ("linux", "aarch64", True, "linux-arm64-musl"),
    ],
)
def test_format_target(os_name: str, arch: str, musl: bool, target: str) -> None:
    assert format_target(os_name, arch, musl=musl) == target


@pytest.mark.parametrize(
    ("os_name", "arch"),
    [("Windows", "ARM64"), ("Linux", "armv7l"), ("FreeBSD", "amd64"), ("", "")],
)
def test_format_target_unsupported(os_name: str, arch: str) -> None:
    with pytest.raises(PyTailwindCssException, match="doesn't publish a standalone binary"):
        format_target(os_name, arch)


@pytest.mark.parametrize(
    ("host_gnu_type", "target"),
    [
        ("x86_64-pc-linux-musl", "linux-x64-musl"),
        ("x86_64-pc-linux-gnu", "linux-x64"),
        (None, "linux-x64"),
    ],
)
def test_detect_target(monkeypatch: pytest.MonkeyPatch, host_gnu_type: str | None, target: str) -> None:
    monkeypatch.setattr(installation.platform, "system", lambda: "Linux")
    monkeypatch.setattr(installation.platform, "machine", lambda: "x86_64")
    monkeypatch.setattr(sysconfig, "get_config_var", lambda name: host_gnu_type)

    assert detect_target() == target
