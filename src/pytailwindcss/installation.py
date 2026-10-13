import hashlib
import http.client
import io
import logging
import os
import pathlib
import platform
import shutil
import ssl
import sys
import sysconfig
import tempfile
import urllib.request
from typing import IO
from urllib.error import HTTPError, URLError

from .exceptions import PyTailwindCssChecksumMismatch, PyTailwindCssException, PyTailwindCssVersionNotFound
from .utils import BIN_DIR_ENV_VAR, get_binary_download_url

logger = logging.getLogger(__name__)

DOWNLOAD_TIMEOUT = 60  # seconds without data before a download is abandoned
CHECKSUMS_FILENAME = "sha256sums.txt"

OS_NAMES = {"linux": "linux", "windows": "windows", "win32": "windows", "darwin": "macos", "macos": "macos"}
ARCH_NAMES = {"amd64": "x64", "x86_64": "x64", "arm64": "arm64", "aarch64": "arm64"}
# Every standalone binary Tailwind CSS publishes: https://github.com/tailwindlabs/tailwindcss/releases
SUPPORTED_TARGETS = {
    "linux-x64",
    "linux-arm64",
    "linux-x64-musl",
    "linux-arm64-musl",
    "macos-x64",
    "macos-arm64",
    "windows-x64.exe",
}


def install_binary(version: str, bin_path: pathlib.Path) -> pathlib.Path:
    """
    Downloads the Tailwind CSS binary, verifies its checksum and atomically
    puts it at bin_path. An existing binary stays in place if anything fails.
    """
    binary_name = f"tailwindcss-{detect_target()}"
    url = get_binary_download_url(version, binary_name)

    try:
        bin_path.parent.mkdir(parents=True, exist_ok=True)
        fd, temp_name = tempfile.mkstemp(prefix=".tailwindcss-", suffix=".part", dir=bin_path.parent)
    except OSError as err:
        raise PyTailwindCssException(
            f"Can't write the Tailwind CSS binary to {bin_path.parent}: {err.strerror}. "
            f"Set {BIN_DIR_ENV_VAR} to a writable directory, or run 'tailwindcss_install' "
            f"where this directory is writable (for example at Docker image build time)."
        ) from err

    temp_path = pathlib.Path(temp_name)
    try:
        with os.fdopen(fd, "w+b") as temp_file:
            print(f"Downloading '{binary_name}' from '{url}'...", file=sys.stderr)
            download(url, temp_file, version)
            temp_file.seek(0)
            actual_sha256 = hashlib.file_digest(temp_file, "sha256").hexdigest()

        expected_sha256 = fetch_expected_sha256(version, binary_name)
        if expected_sha256 is not None and actual_sha256 != expected_sha256:
            raise PyTailwindCssChecksumMismatch(
                f"Checksum mismatch for {binary_name} ({version}): expected {expected_sha256}, got {actual_sha256}. "
                f"The binary was not installed."
            )

        # mkstemp creates 0600 files; the binary must stay runnable by other users, e.g. when
        # it's installed as root at Docker build time and run as an unprivileged user.
        temp_path.chmod(0o755)
        os.replace(temp_path, bin_path)
    except OSError as err:
        # download() maps network failures, so what's left is the local filesystem: a full disk, or on
        # Windows a binary that's still running and can't be replaced.
        temp_path.unlink(missing_ok=True)
        raise PyTailwindCssException(f"Can't write the Tailwind CSS binary to {bin_path}: {err}") from err
    except BaseException:
        temp_path.unlink(missing_ok=True)
        raise

    return bin_path


def fetch_expected_sha256(version: str, binary_name: str) -> str | None:
    """
    Returns the published SHA-256 of binary_name, or None for releases that
    don't publish checksums (everything before v4).
    """
    checksums = io.BytesIO()
    try:
        download(get_binary_download_url(version, CHECKSUMS_FILENAME), checksums, version)
    except PyTailwindCssVersionNotFound:
        logger.warning(
            "Tailwind CSS %s doesn't publish %s; skipping checksum verification.", version, CHECKSUMS_FILENAME
        )
        return None

    # Lines look like "<sha256>  ./tailwindcss-linux-x64".
    for line in checksums.getvalue().decode().splitlines():
        fields = line.split()
        if len(fields) == 2 and fields[1].removeprefix("./") == binary_name:
            return fields[0].lower()
    raise PyTailwindCssChecksumMismatch(
        f"{CHECKSUMS_FILENAME} of Tailwind CSS {version} has no entry for {binary_name}. The binary was not installed."
    )


def download(url: str, dest: IO[bytes], version: str) -> None:
    """
    Streams url into dest, turning network failures into readable exceptions.
    """
    try:
        with open_url(url) as response:
            shutil.copyfileobj(response, dest)
    except HTTPError as err:
        # An HTTPError carries the open error response; close it so it doesn't leak.
        err.close()
        if err.code == 404:
            raise PyTailwindCssVersionNotFound(
                f"Couldn't find {url}. "
                f"Please check if Tailwind CSS {version} exists at https://github.com/tailwindlabs/tailwindcss/releases."
            ) from err
        raise PyTailwindCssException(f"Downloading {url} failed: HTTP {err.code} {err.reason}") from err
    except (URLError, TimeoutError, ConnectionError, ssl.SSLError, http.client.HTTPException) as err:
        reason = err.reason if isinstance(err, URLError) else err
        raise PyTailwindCssException(f"Downloading {url} failed: {reason}") from err


def open_url(url: str) -> IO[bytes]:
    return urllib.request.urlopen(url, timeout=DOWNLOAD_TIMEOUT)


def detect_target() -> str:
    """
    Returns target for current OS and CPU architecture.
    """
    return format_target(os_name=platform.system(), arch=platform.machine(), musl=is_musl())


def is_musl() -> bool:
    # platform.libc_ver() only recognizes musl from Python 3.14 on, so ask how the interpreter was built
    # instead (e.g. "x86_64-pc-linux-musl" on Alpine).
    return "musl" in (sysconfig.get_config_var("HOST_GNU_TYPE") or "")


def format_target(os_name: str, arch: str, musl: bool = False) -> str:
    """
    Formats target name for provided OS name and CPU architecture.
    """
    target_os = OS_NAMES.get(os_name.lower())
    target_arch = ARCH_NAMES.get(arch.lower())
    target = f"{target_os}-{target_arch}"
    if target_os == "linux" and musl:
        target += "-musl"
    elif target_os == "windows":
        target += ".exe"

    if target not in SUPPORTED_TARGETS:
        raise PyTailwindCssException(
            f"Tailwind CSS doesn't publish a standalone binary for {os_name} on {arch}. "
            f"Available targets: {', '.join(sorted(SUPPORTED_TARGETS))}."
        )
    return target
