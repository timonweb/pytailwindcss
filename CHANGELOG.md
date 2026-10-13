# Changelog

## 0.4.0 (unreleased)

### Added

- Downloads are verified against the release's `sha256sums.txt`; a mismatch raises `PyTailwindCssChecksumMismatch` and nothing is installed. Releases without checksums (before v4) install with a warning.
- Alpine and other musl-based Linux systems get the `-musl` Tailwind CSS binary (it needs `apk add libstdc++ libgcc`).
- `TAILWINDCSS_BIN_DIR` environment variable to choose where binaries are stored.
- Type hints and a `py.typed` marker.

### Changed

- Installation is atomic: the binary is downloaded next to its destination and swapped in only after it's verified, so a failed download keeps the previous binary.
- Installed binaries are mode `0755`, so a binary installed as root (e.g. at Docker build time) runs for any user.
- Download progress is printed to stderr instead of stdout, so it no longer mixes with `tailwindcss` output.
- Network failures, HTTP errors other than 404, unsupported platforms, and unwritable binary directories raise `PyTailwindCssException` with a readable message; the CLI commands print it instead of a traceback.
- Downloads time out after 60 seconds without data.
- `run()` raises `PyTailwindCssBinaryNotFound` only when the binary is actually missing; a missing `cwd` now surfaces as the original `FileNotFoundError`.
- README updated for Tailwind CSS v4.

### Fixed

- Windows: the binary is saved as `tailwindcss.exe`, so it can be executed.
- `run(bin_path="...", auto_install=True)` no longer crashes when `bin_path` is a string.
- Temporary download directories are no longer leaked.

## Earlier releases

See the [git tags](https://github.com/timonweb/pytailwindcss/tags).
