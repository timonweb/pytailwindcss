class PyTailwindCssException(Exception):
    pass


class PyTailwindCssBinaryNotFound(PyTailwindCssException):
    pass


class PyTailwindCssVersionNotFound(PyTailwindCssException):
    pass


class PyTailwindCssChecksumMismatch(PyTailwindCssException):
    pass
