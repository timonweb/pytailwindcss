import pytest

import pytailwindcss
from pytailwindcss.exceptions import PyTailwindCssBinaryNotFound
from pytailwindcss.utils import get_bin_path

from .contexts import clean_dir


def test_successful_run():
    """
    It installs the executable and successfully runs a build command.
    """
    with clean_dir(get_bin_path("latest")):
        pytailwindcss.install()
        assert "MIT License | https://tailwindcss.com" in pytailwindcss.run("build")


def test_successful_run_from_custom_bin_path():
    """
    It installs the executable and successfully runs a build command.
    """
    ALTERNATIVE_BIN_PATH = "/tmp/test-bin/tailwindcss"

    with clean_dir(ALTERNATIVE_BIN_PATH):
        pytailwindcss.install(bin_path=ALTERNATIVE_BIN_PATH)
        assert "MIT License | https://tailwindcss.com" in pytailwindcss.run("build", bin_path=ALTERNATIVE_BIN_PATH)


def test_unsuccessful_run():
    """
    It fails to run build command because executable is not installed.
    """
    with clean_dir(get_bin_path("latest")):
        with pytest.raises(PyTailwindCssBinaryNotFound):
            pytailwindcss.run("build")
