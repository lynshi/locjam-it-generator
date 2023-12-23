"""Module for building a Replacer from a CSV file.
"""

import csv
from typing import Any, Callable, Dict


from locjamit.replacer._replacer import Replacer


class CsvReplacer(Replacer):  # pylint: disable=too-few-public-methods
    """Creates a Replacer from a CSV file."""

    def __init__(self, input_csv: str, **kwargs: Any):
        builder = _build_builder(**kwargs)
        super().__init__(input_csv, builder)


def _build_builder(**kwargs: Any) -> Callable[[str], Dict[str, str]]:
    encoding = kwargs.pop("encoding", "utf-8")
    src_header = kwargs.pop("src_header", "source")
    dest_header = kwargs.pop("dest_header", "destination")

    def _builder(input_csv: str):
        translations = {}
        with open(input_csv, newline="", encoding=encoding) as infile:
            reader = csv.DictReader(infile, **kwargs)
            for row in reader:
                src = row[src_header]
                dest = row[dest_header]

                if src in translations:
                    raise RuntimeError(f"'{src}' has been translated twice")

                translations[src] = dest

        print(translations)
        return translations

    return _builder
