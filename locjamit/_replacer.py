# pylint: disable=missing-module-docstring
from __future__ import annotations

import os
from typing import TYPE_CHECKING, Any

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
        **kwargs: Any,
    ):
        if not os.path.isfile(input_file):
            raise FileNotFoundError(f"{input_file} not found")

        overwrite_output = kwargs.pop("overwrite_output", False)
        if not overwrite_output and os.path.isfile(output_file):
            raise FileExistsError(
                f"{output_file} already exists and will be overwritten"
            )

        with open(input_file, encoding="utf-8") as infile:
            self._original_js = infile.read()

        self._translator = translator
        self._output_file = output_file

    @property
    def output_file(self) -> str:
        """Returns the name of the file containing translated output."""
        return self._output_file

    def replace(self):
        """Translate the input JavaScript file and emits the specified output file."""

        translated = []
        for line in self._original_js.splitlines():
            if line.find("`") == -1:
                translated.append(line)
            else:
                assert (
                    line.count("`") == 2
                ), "Expected line containing game text to have exactly 2 '`'"

                prefix, italian, suffix = line.split("`")
                translation = self._translator.translate(italian)

                if translation.status is not TranslationStatus.SUCCESS:
                    translated.append(line)
                else:
                    translated.append("`".join([prefix, translation.value, suffix]))

            translated.append("\n")

        with open(self._output_file, "w", encoding="utf-8") as outfile:
            outfile.writelines(translated)
