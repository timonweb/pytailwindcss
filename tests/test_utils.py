import pathlib

import pytest

import pytailwindcss.utils
from pytailwindcss.utils import (
    BIN_DIR_ENV_VAR,
    format_cli_args,
    get_bin_path,
    get_binary_download_url,
    make_subprocess_run_kwargs,
)


def test_format_cli_args() -> None:
    """
    - It breaks down params provided as string into a list of parameters.
    - It doesn't modify list of parameters.
    """
    args_as_string = "-i ./src/input.css -o ./dist/output.css --watch"
    args_as_list = ["-i", "./src/input.css", "-o", "./dist/output.css", "--watch"]
    assert format_cli_args(args_as_string) == args_as_list
    assert format_cli_args(args_as_list) == args_as_list


def test_make_subprocess_run_kwargs() -> None:
    """
    It makes kwargs for the subprocess.run command taking into account provided parameters.
    """
    assert make_subprocess_run_kwargs(cwd=None)["cwd"] is None
    assert make_subprocess_run_kwargs(cwd="/tmp")["cwd"] == "/tmp"

    assert make_subprocess_run_kwargs(env=None)["env"] is None
    assert make_subprocess_run_kwargs(env={"TAILWINDCSS_VERSION": "v3.0.7"})["env"] == {
        "TAILWINDCSS_VERSION": "v3.0.7"
    }

    assert make_subprocess_run_kwargs(live_output=False).get("capture_output") is True
    assert make_subprocess_run_kwargs(live_output=False).get("check") is True
    assert make_subprocess_run_kwargs(live_output=True).get("capture_output") is None
    assert make_subprocess_run_kwargs(live_output=True).get("check") is None


def test_get_binary_download_url() -> None:
    assert (
        get_binary_download_url("latest", "tailwindcss-linux-x64")
        == "https://github.com/tailwindlabs/tailwindcss/releases/latest/download/tailwindcss-linux-x64"
    )
    assert (
        get_binary_download_url("v3.0.7", "tailwindcss-macos-x64")
        == "https://github.com/tailwindlabs/tailwindcss/releases/download/v3.0.7/tailwindcss-macos-x64"
    )


def test_get_bin_path_defaults_to_package_dir(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv(BIN_DIR_ENV_VAR)
    monkeypatch.setattr(pytailwindcss.utils.platform, "system", lambda: "Linux")

    package_dir = pathlib.Path(pytailwindcss.utils.__file__).parent.resolve()
    assert get_bin_path("v4.0.5") == package_dir / "bin" / "v4.0.5" / "tailwindcss"


def test_get_bin_path_honors_bin_dir_env_var(tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(BIN_DIR_ENV_VAR, str(tmp_path))
    monkeypatch.setattr(pytailwindcss.utils.platform, "system", lambda: "Darwin")

    assert get_bin_path() == tmp_path.resolve() / "latest" / "tailwindcss"


def test_get_bin_path_uses_exe_on_windows(tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(BIN_DIR_ENV_VAR, str(tmp_path))
    monkeypatch.setattr(pytailwindcss.utils.platform, "system", lambda: "Windows")

    assert get_bin_path() == tmp_path.resolve() / "latest" / "tailwindcss.exe"


def test_get_bin_path_resolves_relative_bin_dir(tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """
    A relative TAILWINDCSS_BIN_DIR is made absolute, so run(cwd=...) still finds the binary.
    """
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv(BIN_DIR_ENV_VAR, ".bin")

    assert get_bin_path().parent == (tmp_path / ".bin" / "latest").resolve()


def test_get_bin_path_expands_user(tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.setenv("USERPROFILE", str(tmp_path))
    monkeypatch.setenv(BIN_DIR_ENV_VAR, "~/tailwind")

    assert get_bin_path().parent == (tmp_path / "tailwind" / "latest").resolve()
