import pytest

import pytailwindcss
from pytailwindcss.exceptions import PyTailwindCssBinaryNotFound
from pytailwindcss.utils import get_bin_path

from .contexts import clean_dir


def test_successful_run():
    """
    It installs the executable and successfully runs the CLI.
    """
    with clean_dir(get_bin_path()):
        pytailwindcss.install()
        output = pytailwindcss.run("--help")
        assert "tailwindcss" in output.lower()


def test_successful_run_from_custom_bin_path():
    """
    It installs the executable and successfully runs the CLI from a custom path.
    """
    ALTERNATIVE_BIN_PATH = "/tmp/test-bin/tailwindcss"

    with clean_dir(ALTERNATIVE_BIN_PATH):
        pytailwindcss.install(bin_path=ALTERNATIVE_BIN_PATH)
        output = pytailwindcss.run("--help", bin_path=ALTERNATIVE_BIN_PATH)
        assert "tailwindcss" in output.lower()


def test_unsuccessful_run():
    """
    It fails to run build command because executable is not installed.
    """
    with clean_dir(get_bin_path()):
        with pytest.raises(PyTailwindCssBinaryNotFound):
            pytailwindcss.run("build")
