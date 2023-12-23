# pylint: disable=missing-module-docstring

from enum import Enum
import os
from typing import Callable, Dict, Optional

from locjamit.translation._stats import TranslationStatistics


class TranslationStatus(Enum):  # pylint: disable=missing-class-docstring
    SUCCESS = 0
    NOT_FOUND = 1


class TranslationResult:  # pylint: disable=missing-class-docstring
    def __init__(
        self, source: str, status: TranslationStatus, result: Optional[str] = None
    ):
        if result is not None and status is not TranslationStatus.SUCCESS:
            raise ValueError(
                f"Cannot provide result when status is not {TranslationStatus.SUCCESS}"
            )

        if status is TranslationStatus.SUCCESS and not result:
            raise ValueError(
                f"Result canot be None when status is {TranslationStatus.SUCCESS}"
            )

        self._source = source
        self._status = status
        self._value = result

    @property
    def source(self) -> str:
        """Returns the source string."""
        return self._source

    @property
    def status(self) -> TranslationStatus:  # pylint: disable=missing-function-docstring
        return self._status

    @property
    def value(self) -> str:
        """Returns the translation value.

        Raises a RuntimeError if the status is not SUCCESS.

        :raises RuntimeError: When the status is not SUCCESS.
        :return: The translation value.
        :rtype: str
        """
        if self.status is not TranslationStatus.SUCCESS:
            raise RuntimeError(f"Cannot get result when status is {self.status}")

        assert self._value
        return self._value


class Translator:
    """Base class for replacing text."""

    def __init__(self, input_file: str, builder: Callable[[str], Dict[str, str]]):
        if not os.path.isfile(input_file):
            raise FileNotFoundError(f"{input_file} not found")

        self._translations = builder(input_file)
        self._stats = TranslationStatistics(self._translations)

    def translate(self, src: str) -> TranslationResult:
        """Returns the translation given a source string.

        :param src: A string in the original language.
        :type src: str
        :return: A string in the new language.
        :rtype: str
        """
        if src not in self._translations:
            return TranslationResult(src, TranslationStatus.NOT_FOUND)

        self._stats.count_use(src)
        return TranslationResult(
            src, TranslationStatus.SUCCESS, self._translations[src]
        )

    def get_stats(self) -> TranslationStatistics:
        return self._stats
