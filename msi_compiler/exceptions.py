import logging

from logging import NOTSET, DEBUG, INFO, WARN, ERROR, CRITICAL


NO_EXIT = 0
EXIT_EXPECTED = 1

# Log levels are ints, we want SUCCESS to show if INFO shows (value is 21)
SUCCESS = INFO + 1


class MsiCompilerException(BaseException):
    exit_code = NO_EXIT
    level = NOTSET

    def __init__(self, message: str):
        self.message = message


class MsiCompilerWarning(MsiCompilerException):
    exit_code = EXIT_EXPECTED
    level = ERROR


class MsiCompilerError(MsiCompilerException, Warning):
    exit_code = NO_EXIT
    level = WARN


class ConfigPropertyError(MsiCompilerError):
    pass


class ConfigPropertyWarning(MsiCompilerWarning):
    pass