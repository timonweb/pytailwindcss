import os
import subprocess
import sys
from typing import cast

import pytailwindcss
from pytailwindcss.exceptions import PyTailwindCssException

# Shell convention for "terminated by Ctrl+C" (128 + SIGINT).
INTERRUPTED_EXIT_CODE = 130


def install() -> None:
    try:
        pytailwindcss.install(os.environ.get("TAILWINDCSS_VERSION", "latest"))
    except PyTailwindCssException as err:
        sys.exit(f"tailwindcss_install: {err}")
    except KeyboardInterrupt:
        sys.exit(INTERRUPTED_EXIT_CODE)


def main() -> None:
    try:
        completed_process = pytailwindcss.run(sys.argv[1:], env=os.environ.copy(), live_output=True, auto_install=True)
    except PyTailwindCssException as err:
        sys.exit(f"tailwindcss: {err}")
    except KeyboardInterrupt:
        # Ctrl+C reaches the whole process group, so tailwindcss gets it too and stops by itself
        # (e.g. ending --watch); only the waiting Python process needs to exit quietly.
        sys.exit(INTERRUPTED_EXIT_CODE)
    # live_output=True always returns the CompletedProcess.
    sys.exit(cast(subprocess.CompletedProcess[bytes], completed_process).returncode)


if __name__ == "__main__":
    main()
