import logging
import os
import pathlib
import platform
import shutil
import stat
import urllib.request
from tempfile import mkdtemp
from urllib.error import HTTPError

from .exceptions import PyTailwindCssVersionNotFound
from .utils import get_binary_download_url

logger = logging.getLogger(__name__)


def install_binary(version, bin_path):
    """
    Handles installation process of the Tailwind CSS Binary.
    Downloads binary, copies it and makes it executable.
    """
    if os.path.isfile(bin_path):
        logger.info(f"Removing old {bin_path}")
        os.remove(bin_path)
    os.makedirs(bin_path.parent, exist_ok=True)

    binary_name = f"tailwindcss-{detect_target()}"
    url = get_binary_download_url(version, binary_name)

    try:
        logger.info(f"Downloading {binary_name} from {url}")
        print(f"Downloading '{binary_name}' from '{url}'...")
        downloaded_filepath = download_file(url)
    except HTTPError as err:
        if err.code == 404:
            raise PyTailwindCssVersionNotFound(
                f"Couldn't find Tailwind CSS binary for version {version}. "
                f"Please check if this version exists at "
                f"https://github.com/tailwindlabs/tailwindcss/releases."
            )
        else:
            raise err

    logger.info(f"Copying {downloaded_filepath} to {bin_path}")
    tailwindcss_bin_path = shutil.copy(downloaded_filepath, bin_path)

    # Sets chmod +x for the binary to make it executable
    tailwindcss_bin_path.chmod(tailwindcss_bin_path.stat().st_mode | stat.S_IEXEC)
    return tailwindcss_bin_path


def detect_target():
    """
    Returns target for current OS and CPU architecture.

    # Available tailwindcss targets: https://github.com/tailwindlabs/tailwindcss/releases
    """
    return format_target(os_name=platform.system(), arch=platform.machine())


def format_target(os_name, arch):
    """
    Formats target name for provided OS name and CPU architecture.
    """
    os_name = os_name.lower().replace("win32", "windows").replace("darwin", "macos")
    extension = ".exe" if os_name == "windows" else ""

    assert os_name in ["linux", "windows", "macos"]

    return {
        "amd64": f"{os_name}-x64{extension}",
        "x86_64": f"{os_name}-x64{extension}",
        "arm64": f"{os_name}-arm64",
        "aarch64": f"{os_name}-arm64",
    }[arch.lower()]


def download_file(url):
    """
    Downloads a file to a temp directory
    """
    temp_dir = mkdtemp()
    working_dir = pathlib.Path(temp_dir)
    dest_filename = working_dir / os.path.basename(url)

    urllib.request.urlretrieve(url, str(dest_filename))

    return dest_filename
