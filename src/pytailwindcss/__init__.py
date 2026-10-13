import os
import pathlib
import subprocess
from collections.abc import Mapping, Sequence
from typing import TypeAlias

from .exceptions import PyTailwindCssBinaryNotFound
from .installation import install_binary
from .utils import format_cli_args, get_bin_path, make_subprocess_run_kwargs

StrPath: TypeAlias = str | os.PathLike[str]


def run(
    tailwindcss_cli_args: Sequence[str] | str | None = None,
    cwd: StrPath | None = None,
    bin_path: StrPath | None = None,
    env: Mapping[str, str] | None = None,
    live_output: bool = False,
    auto_install: bool = False,
    version: str | None = None,
) -> str | subprocess.CompletedProcess[bytes]:
    """
    Runs the Tailwind CSS binary from Python.

    tailwindcss_cli_args are passed to the binary, either as a list or as a
    shell-style string. env replaces the binary's environment; its
    TAILWINDCSS_VERSION picks the version when version isn't given ('latest'
    otherwise). With live_output the binary writes straight to the terminal and
    the CompletedProcess is returned; without it, the captured stdout is
    returned and a non-zero exit raises subprocess.CalledProcessError.
    auto_install downloads the binary first if it's missing.
    """
    if version is None:
        version = env.get("TAILWINDCSS_VERSION", "latest") if env else "latest"

    bin_path = get_bin_path(version) if bin_path is None else pathlib.Path(bin_path)

    if auto_install and not bin_path.exists():
        install(version, bin_path)

    args = format_cli_args(tailwindcss_cli_args or "")
    kwargs = make_subprocess_run_kwargs(cwd, env, live_output)
    try:
        output = subprocess.run([str(bin_path), *args], **kwargs)
    except FileNotFoundError as err:
        # A missing cwd raises FileNotFoundError too; only a missing binary means "not installed".
        if bin_path.exists():
            raise
        raise PyTailwindCssBinaryNotFound(
            f"Tailwind CSS binary not found at {bin_path}. Run 'tailwindcss_install' or pass auto_install=True."
        ) from err

    if live_output:
        return output
    return output.stdout.decode().strip()


def install(version: str | None = None, bin_path: StrPath | None = None) -> pathlib.Path:
    """
    Installs the Tailwind CSS binary and returns its path.

    version defaults to 'latest'; bin_path defaults to the location run() looks in.
    """
    if version is None:
        version = "latest"
    bin_path = get_bin_path(version) if bin_path is None else pathlib.Path(bin_path)
    return install_binary(version, bin_path)
