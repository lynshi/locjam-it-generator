from enum import Enum
import os
from typing import Optional


class ReplaceStatus(Enum):
    SUCCESS = 0
    NOT_FOUND = 1


class ReplaceResult:
    def __init__(self, status: ReplaceStatus, result: Optional[str] = None):
        if result is not None and status is not ReplaceStatus.SUCCESS:
            raise ValueError(f"Cannot provide result when status is not {ReplaceStatus.SUCCESS}")
        
        if status is ReplaceStatus.SUCCESS and not result:
            raise ValueError(f"Result canot be None when status is {ReplaceStatus.SUCCESS}")

        self._status = status
        self._result = result

    @property
    def status(self) -> ReplaceStatus:
        return self._status

    @property
    def result(self) -> str:
        if self.status is not ReplaceStatus.SUCCESS:
            raise RuntimeError(f"Cannot get result when status is {self.status}")
        
        assert self._result
        return self._result


class Replacer:
    """Base class for replacing text.
    """

    def __init__(self, input_file: str):
        if not os.path.isfile(input_file):
            raise FileNotFoundError(f"{input_file} not found")
        
        self._input_file = input_file
        self._translations = {}

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
