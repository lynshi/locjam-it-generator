import csv
import os
from typing import Any, Callable, Dict

from charset_normalizer import from_path

from locjamit.replacer._replacer import Replacer


class CsvReplacer(Replacer):
    def __init__(self, input_csv: str, **kwargs: Any):
        builder = _build_builder(input_csv, **kwargs)
        super().__init__(input_csv, builder)


def _build_builder(input_csv: str, **kwargs: Any) -> Callable[[str], Dict[str, str]]:
    encoding = kwargs.pop("encoding", _get_encoding(input_csv))
    src_header = kwargs.pop("src_header", "source")
    dest_header = kwargs.pop("dest_header", "destination")

    def _builder(input_csv: str):
        translations = {}
        with open(input_csv, newline='', encoding=encoding) as infile:
            reader = csv.DictReader(infile)
            for row in reader:
                src = row[src_header]
                dest = row[dest_header]
                
                if src in translations:
                    raise RuntimeError(f"'{src}' has been translated twice")
                
                translations[src] = dest

        return translations
    
    return _builder


def _get_encoding(file: str) -> str:
    if not os.path.isfile(file):
        raise FileNotFoundError(f"{file} not found")

    matches = from_path(file)
    best = matches.best()

    if best is None:
        raise RuntimeError(f"Could not determine encoding of {file}")

    return best.encoding
