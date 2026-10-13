import subprocess

import pytest

import pytailwindcss
from pytailwindcss import __main__
from pytailwindcss.exceptions import PyTailwindCssException


def test_main_exits_with_binary_return_code(monkeypatch: pytest.MonkeyPatch) -> None:
    calls = []

    def fake_run(*args: object, **kwargs: object) -> subprocess.CompletedProcess[bytes]:
        calls.append((args, kwargs))
        return subprocess.CompletedProcess(args=["tailwindcss"], returncode=3)

    monkeypatch.setattr(pytailwindcss, "run", fake_run)
    monkeypatch.setattr(__main__.sys, "argv", ["tailwindcss", "-i", "in.css"])

    with pytest.raises(SystemExit) as exc_info:
        __main__.main()

    assert exc_info.value.code == 3
    assert calls[0][0] == (["-i", "in.css"],)
    assert calls[0][1]["live_output"] is True
    assert calls[0][1]["auto_install"] is True


def test_main_reports_errors_without_traceback(monkeypatch: pytest.MonkeyPatch) -> None:
    def failing_run(*args: object, **kwargs: object) -> None:
        raise PyTailwindCssException("no network")

    monkeypatch.setattr(pytailwindcss, "run", failing_run)
    monkeypatch.setattr(__main__.sys, "argv", ["tailwindcss"])

    with pytest.raises(SystemExit) as exc_info:
        __main__.main()

    assert exc_info.value.code == "tailwindcss: no network"


def test_install_uses_version_env_var(monkeypatch: pytest.MonkeyPatch) -> None:
    versions = []
    monkeypatch.setattr(pytailwindcss, "install", lambda version=None: versions.append(version))
    monkeypatch.setenv("TAILWINDCSS_VERSION", "v4.0.5")

    __main__.install()

    assert versions == ["v4.0.5"]


def test_install_defaults_to_latest(monkeypatch: pytest.MonkeyPatch) -> None:
    versions = []
    monkeypatch.setattr(pytailwindcss, "install", lambda version=None: versions.append(version))
    monkeypatch.delenv("TAILWINDCSS_VERSION", raising=False)

    __main__.install()

    assert versions == ["latest"]


def test_install_reports_errors_without_traceback(monkeypatch: pytest.MonkeyPatch) -> None:
    def failing_install(version: str | None = None) -> None:
        raise PyTailwindCssException("no network")

    monkeypatch.setattr(pytailwindcss, "install", failing_install)

    with pytest.raises(SystemExit) as exc_info:
        __main__.install()

    assert exc_info.value.code == "tailwindcss_install: no network"


def test_main_exits_quietly_on_ctrl_c(monkeypatch: pytest.MonkeyPatch) -> None:
    def interrupted_run(*args: object, **kwargs: object) -> None:
        raise KeyboardInterrupt

    monkeypatch.setattr(pytailwindcss, "run", interrupted_run)
    monkeypatch.setattr(__main__.sys, "argv", ["tailwindcss", "--watch"])

    with pytest.raises(SystemExit) as exc_info:
        __main__.main()

    assert exc_info.value.code == 130


def test_install_exits_quietly_on_ctrl_c(monkeypatch: pytest.MonkeyPatch) -> None:
    def interrupted_install(version: str | None = None) -> None:
        raise KeyboardInterrupt

    monkeypatch.setattr(pytailwindcss, "install", interrupted_install)

    with pytest.raises(SystemExit) as exc_info:
        __main__.install()

    assert exc_info.value.code == 130
