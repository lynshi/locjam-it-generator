# pylint: disable=missing-module-docstring

from enum import Enum
import os
from typing import Callable, Dict, Optional


class ReplaceStatus(Enum):  # pylint: disable=missing-class-docstring
    SUCCESS = 0
    NOT_FOUND = 1


class ReplaceResult:  # pylint: disable=missing-class-docstring
    def __init__(self, status: ReplaceStatus, result: Optional[str] = None):
        if result is not None and status is not ReplaceStatus.SUCCESS:
            raise ValueError(
                f"Cannot provide result when status is not {ReplaceStatus.SUCCESS}"
            )

        if status is ReplaceStatus.SUCCESS and not result:
            raise ValueError(
                f"Result canot be None when status is {ReplaceStatus.SUCCESS}"
            )

        self._status = status
        self._result = result

    @property
    def status(self) -> ReplaceStatus:  # pylint: disable=missing-function-docstring
        return self._status

    @property
    def value(self) -> str:
        """Returns the replacement value.

        Raises a RuntimeError if the status is not SUCCESS.

        :raises RuntimeError: When the status is not SUCCESS.
        :return: The replacement value.
        :rtype: str
        """
        if self.status is not ReplaceStatus.SUCCESS:
            raise RuntimeError(f"Cannot get result when status is {self.status}")

        assert self._result
        return self._result


class Replacer:  # pylint: disable=too-few-public-methods
    """Base class for replacing text."""

    def __init__(self, input_file: str, builder: Callable[[str], Dict[str, str]]):
        if not os.path.isfile(input_file):
            raise FileNotFoundError(f"{input_file} not found")

        self._translations = builder(input_file)

    def replace(self, src: str) -> ReplaceResult:
        """Returns the translation given a source string.

        :param src: A string in the original language.
        :type src: str
        :return: A string in the new language.
        :rtype: str
        """
        if src not in self._translations:
            return ReplaceResult(ReplaceStatus.NOT_FOUND)

        return ReplaceResult(ReplaceStatus.SUCCESS, self._translations[src])
