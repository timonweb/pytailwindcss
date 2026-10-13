import os
import subprocess
import sys
from typing import cast

import pytailwindcss
from pytailwindcss.exceptions import PyTailwindCssException


def install() -> None:
    try:
        pytailwindcss.install(os.environ.get("TAILWINDCSS_VERSION", "latest"))
    except PyTailwindCssException as err:
        sys.exit(f"tailwindcss_install: {err}")


def main() -> None:
    try:
        completed_process = pytailwindcss.run(sys.argv[1:], env=os.environ.copy(), live_output=True, auto_install=True)
    except PyTailwindCssException as err:
        sys.exit(f"tailwindcss: {err}")
    # live_output=True always returns the CompletedProcess.
    sys.exit(cast(subprocess.CompletedProcess[bytes], completed_process).returncode)


if __name__ == "__main__":
    main()
