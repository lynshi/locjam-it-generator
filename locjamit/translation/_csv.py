"""Module for building a Translator from a CSV file.
"""

import csv
from typing import Any, Callable, Dict, List


from locjamit.translation._translator import Translator


class CsvConfig:  # pylint: disable=too-few-public-methods
    """Parses configuration for a CsvTranslator."""

    def __init__(self, config: Dict[str, Any]):
        self._config = config

    def as_kwargs(self) -> Dict[str, Any]:  # pylint: disable=missing-function-docstring
        config = {}

        fields = ["encoding", "src_header", "dest_header", "delimiter"]
        for field in fields:
            if field in self._config:
                config[field] = self._config[field]

        return config


class CsvTranslator(Translator):  # pylint: disable=too-few-public-methods
    """Creates a Translator from a CSV file."""

    def __init__(self, input_csv: str, **kwargs: Any):
        builder = self._build_builder(**kwargs)
        super().__init__(input_csv, builder)

    def _build_builder(
        self, **kwargs: Any
    ) -> Callable[[str, List[str]], Dict[str, str]]:
        encoding = kwargs.pop("encoding", "utf-8")
        src_header = kwargs.pop("src_header", "source")
        dest_header = kwargs.pop("dest_header", "destination")

        def _builder(input_csv: str, duplicates: List[str]):
            translations = {}
            with open(input_csv, newline="", encoding=encoding) as infile:
                reader = csv.DictReader(infile, **kwargs)
                for row in reader:
                    src = row[src_header]
                    dest = row[dest_header]

                    if src in duplicates:
                        continue

                    if src in translations and dest != translations[src]:
                        duplicates.append(src)
                        del translations[src]
                        continue

                    translations[src] = dest

            return translations

        return _builder
