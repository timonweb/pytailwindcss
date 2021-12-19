import os
import pathlib

from utils import get_binary_download_url

import pytailwindcss
from pytailwindcss.utils import (
    format_cli_args,
    get_bin_path,
    make_subprocess_run_kwargs,
)


def test_get_bin_path():
    """
    It returns correct binary path that includes binary version.
    """
    pytailwindcss_lib_path = pathlib.Path(pytailwindcss.__file__)
    get_bin_path("latest") == pytailwindcss_lib_path / "bin/latest/tailwindcss"
    get_bin_path("v3.0.7") == pytailwindcss_lib_path / "bin/v3.0.7/tailwindcss"


def test_format_cli_args():
    """
    - It breaks down params provided as string into a list of parameters.
    - It doesn't modify list of parameters.
    """
    args_as_string = "-i ./src/input.css -o ./dist/output.css --watch"
    args_as_list = ["-i", "./src/input.css", "-o", "./dist/output.css", "--watch"]
    assert format_cli_args(args_as_string) == args_as_list
    assert format_cli_args(args_as_list) == args_as_list


def test_make_subprocess_run_kwargs():
    """
    It makes kwargs for the  subprocess.run command taking into account provided parameters.
    """
    assert make_subprocess_run_kwargs(cwd=None)["cwd"] == os.getcwd()
    assert make_subprocess_run_kwargs(cwd="/tmp")["cwd"] == "/tmp"

    assert make_subprocess_run_kwargs(env=None)["env"] == {}
    assert make_subprocess_run_kwargs(env={"TAILWINDCSS_VERSION": "v3.0.7"})["env"] == {
        "TAILWINDCSS_VERSION": "v3.0.7"
    }

    assert make_subprocess_run_kwargs(live_output=False).get("capture_output") is True
    assert make_subprocess_run_kwargs(live_output=False).get("check") is True
    assert make_subprocess_run_kwargs(live_output=True).get("capture_output") is None
    assert make_subprocess_run_kwargs(live_output=True).get("check") is None


def test_get_binary_download_url():
    assert (
        get_binary_download_url("latest", "tailwindcss-linux-x64")
        == "https://github.com/tailwindlabs/tailwindcss/releases/latest/download/tailwindcss-linux-x64"
    )
    assert (
        get_binary_download_url("v3.0.7", "tailwindcss-macos-x64")
        == "https://github.com/tailwindlabs/tailwindcss/releases/download/v3.0.7/tailwindcss-macos-x64"
    )
