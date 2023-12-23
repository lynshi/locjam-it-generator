# pylint: disable=missing-module-docstring
from __future__ import annotations

import os
from typing import TYPE_CHECKING, Any

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
        self._translated_js = ""
        self._output_file = output_file
        self._translation_complete = False

    def replace(self):
        """Translate the input JavaScript file and emits the specified output file."""

    def summarize(self):
        """Summarizes the results."""

        if not self._translation_complete:
            raise RuntimeError(
                "Cannot generate a summary while translation is incomplete"
            )
