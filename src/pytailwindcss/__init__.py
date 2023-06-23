import pathlib
import subprocess
from typing import Union

from .exceptions import PyTailwindCssBinaryNotFound
from .installation import install_binary
from .utils import ensure_is_pathlib_path, format_cli_args, get_bin_path, make_subprocess_run_kwargs


def run(
    tailwindcss_cli_args: Union[list, str] = None,
    cwd: Union[pathlib.Path, str] = None,
    bin_path: Union[pathlib.Path, str] = None,
    env: dict = None,
    live_output: bool = False,
    auto_install: bool = False,
    version: str = None,
):
    """
    Main entry point to the Tailwind CSS binary.

    Use it to run Tailwind CSS binary from Python.

    @param tailwindcss_cli_args: a string or list of arguments to be passed to
    Tailwindcss binary
    @param cwd: current working directory
    @param bin_path: a path to the tailwindcss executable
    @param env: an object of environment variables to be passed to
    the tailwindcss executable
    @param live_output: if set to 'True' a live output of the tailwindcss
    binary exec will be printed on the screen. If set to 'False', only
    the result of the command will be printed out.
    @param auto_install: if set to 'True', tailwindcss binary will be installed
    automatically upon the first command call.
    @param version: sets version of the tailwindcss binary.
    Defaults to the 'latest' if not provided.
    """
    if version is None:
        version = env.get("TAILWINDCSS_VERSION", "latest") if env else "latest"

    if bin_path is None:
        bin_path = get_bin_path(version)

    if auto_install and not bin_path.exists():
        install(version, bin_path)

    try:
        tailwindcss_cli_args = format_cli_args(tailwindcss_cli_args or "")
        kwargs = make_subprocess_run_kwargs(cwd, env, live_output)
        output = subprocess.run([str(bin_path)] + tailwindcss_cli_args, **kwargs)
        if live_output:
            return output
        return output.stdout.decode().strip()
    except FileNotFoundError as err:
        raise PyTailwindCssBinaryNotFound(err)


def install(version: str = None, bin_path: Union[pathlib.Path, str] = None):
    """
    Installs tailwindcss binary.
    @param version: sets version of the tailwindcss binary. Defaults to the 'latest' if not provided.
    @param bin_path: sets bin path for the tailwindcss binary. Sets default location is not provided.
    @return:
    """
    if version is None:
        version = "latest"
    if bin_path is None:
        bin_path = get_bin_path(version)
    return install_binary(version, ensure_is_pathlib_path(bin_path))
