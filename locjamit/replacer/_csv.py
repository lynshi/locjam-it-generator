import csv
import os
import sys
from typing import Any

from charset_normalizer import from_path

from locjamit.replacer._replacer import Replacer


class CsvReplacer(Replacer):
    def __init__(self, input_csv: str, **kwargs: Any):
        super().__init__(input_csv)
        
        encoding = kwargs.pop("encoding", _get_encoding(input_csv))
        src_header = kwargs.pop("src_header", "source")
        dest_header = kwargs.pop("dest_header", "destination")

        with open(input_csv, newline='', encoding=encoding) as infile:
            reader = csv.DictReader(infile)
            for row in reader:
                src = row[src_header]
                dest = row[dest_header]
                
                if src in self._translations:
                    raise RuntimeError(f"'{src}' has been translated twice")
                
                self._translations[src] = dest


def _get_encoding(file: str) -> str:
    matches = from_path(file)
    best = matches.best()

    if best is None:
        raise RuntimeError(f"Could not determine encoding of {file}")

    return best.encoding
