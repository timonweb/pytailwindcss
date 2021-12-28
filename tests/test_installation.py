import os.path
import platform

import pytailwindcss
from pytailwindcss.installation import detect_target, format_target
from pytailwindcss.utils import get_bin_path

from .contexts import clean_dir

BIN_PATH = get_bin_path()


def test_install():
    """
    It installs 'latest' binary at the expected path.
    """
    with clean_dir(get_bin_path()):
        pytailwindcss.install(bin_path=BIN_PATH)
        assert os.path.isfile(BIN_PATH), f"File installed at {BIN_PATH}"


def test_version_install():
    """
    It installs versioned binary at the expected path.
    """
    VERSIONED_BIN_PATH = get_bin_path()
    with clean_dir(VERSIONED_BIN_PATH):
        pytailwindcss.install(version="v3.0.5")
        assert "3.0.5" in pytailwindcss.run(), "v3.0.5 is installed"


def test_alternative_install():
    """
    It installs binary at the alternative path.
    """
    ALTERNATIVE_BIN_PATH = "/tmp/test-bin/tailwindcss"
    with clean_dir(ALTERNATIVE_BIN_PATH):
        pytailwindcss.install(bin_path=ALTERNATIVE_BIN_PATH)
        assert os.path.isfile(ALTERNATIVE_BIN_PATH), f"File installed at {ALTERNATIVE_BIN_PATH}"


def test_target():
    """
    It detects target for the test machine.
    """
    if platform.system() == "darwin":
        assert detect_target() == "macos-x64"
    elif platform.system() == "linux":
        assert detect_target() == "linux-x64"
    elif platform.system() == "win32":
        assert detect_target() == "windows-x64.exe"


def test_format_target():
    """
    It formats target names using os name and arch name.
    """
    assert format_target("win32", "x86_64") == "windows-x64.exe"
    assert format_target("darwin", "x86_64") == "macos-x64"
    assert format_target("darwin", "arm64") == "macos-arm64"
    assert format_target("linux", "x86_64") == "linux-x64"
    assert format_target("linux", "amd64") == "linux-x64"


def test_format_target_uppercase_arch():
    """
    It formats target names using os name and arch name,
    even if arch name is uppercase
    """
    assert format_target("win32", "X86_64") == "windows-x64.exe"
    assert format_target("darwin", "X86_64") == "macos-x64"
    assert format_target("darwin", "ARM64") == "macos-arm64"
    assert format_target("linux", "X86_64") == "linux-x64"
    assert format_target("linux", "AMD64") == "linux-x64"
