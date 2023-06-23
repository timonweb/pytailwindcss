import os
import pathlib
import shlex


def make_subprocess_run_kwargs(cwd=None, env=None, live_output=False):
    """
    Creates an object with additional kwargs for the subprocess.run command.
    """
    opts = {
        "cwd": cwd or os.getcwd(),
        "env": env or {},
    }
    if live_output is False:
        opts.update(
            {
                "capture_output": True,
                "check": True,
            }
        )
    return opts


def format_cli_args(cli_args):
    """
    Formats cli_args as list if they're string.
    """
    if isinstance(cli_args, str):
        return shlex.split(cli_args)
    return cli_args


def get_bin_path(version="latest"):
    """
    Returns a path for the tailwindcss binary.
    """
    return pathlib.Path(__file__).parent.resolve() / "bin" / version / "tailwindcss"


def ensure_is_pathlib_path(path):
    if isinstance(path, str):
        return pathlib.Path(path)
    return path


def get_binary_download_url(version, binary_name):
    """
    Get a binary download URL for a version and binary_name
    """
    if version == "latest":
        return f"https://github.com/tailwindlabs/tailwindcss/releases/latest/download/{binary_name}"
    return f"https://github.com/tailwindlabs/tailwindcss/releases/download/{version}/{binary_name}"
