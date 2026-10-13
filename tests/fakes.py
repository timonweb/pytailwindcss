import email.message
import hashlib
import io
from urllib.error import HTTPError

from pytailwindcss import installation
from pytailwindcss.utils import get_binary_download_url

FAKE_TARGET = "linux-x64"
FAKE_BINARY_NAME = f"tailwindcss-{FAKE_TARGET}"
FAKE_BINARY = b'#!/bin/sh\necho "fake tailwindcss $@"\n'


class FakeRelease:
    """
    Stands in for GitHub release downloads: unknown URLs answer 404.
    """

    def __init__(self) -> None:
        self.responses: dict[str, bytes | Exception] = {}

    def add_binary(self, content: bytes = FAKE_BINARY) -> None:
        self.responses[get_binary_download_url("latest", FAKE_BINARY_NAME)] = content

    def add_checksums(self, content: bytes) -> None:
        self.responses[get_binary_download_url("latest", installation.CHECKSUMS_FILENAME)] = content

    def add_valid_checksums(self) -> None:
        digest = hashlib.sha256(FAKE_BINARY).hexdigest()
        self.add_checksums(f"{'0' * 64}  ./tailwindcss-macos-x64\n{digest}  ./{FAKE_BINARY_NAME}\n".encode())

    def fail_binary(self, error: Exception) -> None:
        self.responses[get_binary_download_url("latest", FAKE_BINARY_NAME)] = error

    def open_url(self, url: str) -> io.BytesIO:
        if url not in self.responses:
            raise HTTPError(url, 404, "Not Found", email.message.Message(), None)
        response = self.responses[url]
        if isinstance(response, Exception):
            raise response
        return io.BytesIO(response)
