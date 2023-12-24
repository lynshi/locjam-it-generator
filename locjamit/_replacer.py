# pylint: disable=missing-module-docstring
from __future__ import annotations

import os
from typing import TYPE_CHECKING, Any, List

from loguru import logger

from locjamit.translation import TranslationStatus

if TYPE_CHECKING:  # pragma: no cover
    from locjamit.translation import Translator


class Replacer:
    """The Replacer is used to replace Italian strings in the original JavaScript game file with
    translated strings loaded from the provided Translator.
    """

    def __init__(
        self,
        *,
        input_file: str,
        output_file: str,
        translator: Translator,
    ):
        if not os.path.isfile(input_file):
            raise FileNotFoundError(f"{input_file} not found")

        with open(input_file, encoding="utf-8") as infile:
            self._original_js = infile.read()

        self._translator = translator
        self._output_file = output_file
        self._misses = set()
        self._translated = False

    @property
    def output_file(self) -> str:
        """Returns the name of the file containing translated output."""
        return self._output_file

    def replace(self):
        """Translate the input JavaScript file and emits the specified output file.

        Must only be called once.
        """

        assert self._translated is False, "`replace` can only be called once"

        try:
            translated = []
            for line in self._original_js.splitlines():
                if line.find("`") == -1:
                    translated.append(line)
                    logger.debug(f"Contains no Italian: '{line}'")
                else:
                    assert (
                        line.count("`") == 2
                    ), "Expected line containing game text to have exactly 2 '`'"

                    prefix, italian, suffix = line.split("`")
                    translation = self._translator.translate(italian)

                    if translation.status is not TranslationStatus.SUCCESS:
                        translated.append(line)
                        self._misses.add(italian)
                    else:
                        translated.append("`".join([prefix, translation.value, suffix]))

                translated.append("\n")

            with open(self._output_file, "w", encoding="utf-8") as outfile:
                outfile.writelines(translated)

        finally:
            self._translated = True

    @property
    def misses(self) -> List[str]:
        """Returns strings that were missed in the translation."""
        return sorted(self._misses)
