import os
import pathlib
import platform
import shlex
from collections.abc import Mapping, Sequence
from typing import Any

BIN_DIR_ENV_VAR = "TAILWINDCSS_BIN_DIR"


def make_subprocess_run_kwargs(
    cwd: str | os.PathLike[str] | None = None,
    env: Mapping[str, str] | None = None,
    live_output: bool = False,
) -> dict[str, Any]:
    """
    Creates an object with additional kwargs for the subprocess.run command.
    """
    opts: dict[str, Any] = {
        "cwd": cwd,
        "env": env or None,
    }
    if live_output is False:
        opts.update(
            {
                "capture_output": True,
                "check": True,
            }
        )
    return opts


def format_cli_args(cli_args: Sequence[str] | str) -> list[str]:
    """
    Formats cli_args as list if they're string.
    """
    if isinstance(cli_args, str):
        return shlex.split(cli_args)
    return list(cli_args)


def get_bin_path(version: str = "latest") -> pathlib.Path:
    """
    Returns a path for the tailwindcss binary.

    Binaries live inside the package directory (one per virtualenv) unless
    the TAILWINDCSS_BIN_DIR environment variable points elsewhere.
    """
    bin_dir = os.environ.get(BIN_DIR_ENV_VAR)
    # Resolved, because run(cwd=...) would otherwise look for a relative binary path inside cwd.
    root = pathlib.Path(bin_dir).expanduser().resolve() if bin_dir else pathlib.Path(__file__).parent.resolve() / "bin"
    # Windows' CreateProcess appends ".exe" to extensionless paths, so the binary must carry it.
    name = "tailwindcss.exe" if platform.system() == "Windows" else "tailwindcss"
    return root / version / name


def get_binary_download_url(version: str, binary_name: str) -> str:
    """
    Get a binary download URL for a version and binary_name
    """
    if version == "latest":
        return f"https://github.com/tailwindlabs/tailwindcss/releases/latest/download/{binary_name}"
    return f"https://github.com/tailwindlabs/tailwindcss/releases/download/{version}/{binary_name}"
