import os
import sys

import pytailwindcss


def install() -> None:
    pytailwindcss.install(os.environ.get("TAILWINDCSS_VERSION", "latest"))


def main() -> None:
    env = os.environ.copy()
    completed_process = pytailwindcss.run(
        sys.argv[1:],
        env=env,
        live_output=True,
        auto_install=True,
        version=os.environ.get("TAILWINDCSS_VERSION", "latest"),
    )
    sys.exit(completed_process.returncode)


if __name__ == "__main__":
    main()
