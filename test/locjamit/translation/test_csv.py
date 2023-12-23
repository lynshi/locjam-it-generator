import os

import pytest

from locjamit.translation import CsvTranslator


def test_init(tmpdir: str):
    translations = {
        "hello": "你好",
        "world": "世界",
    }

    input_csv = os.path.join(tmpdir, "input.csv")
    with open(input_csv, "w", encoding="utf-8") as outfile:
        outfile.write("source,destination")

        for k, v in translations.items():
            outfile.write(f"\n{k},{v}")

    translator = CsvTranslator(input_csv)
    assert translator._translations == translations


def test_init_with_kwargs(tmpdir: str):
    translations = {
        "hello": "你好",
        "world": "世界",
    }

    src_header = "src"
    dest_header = "dest"
    delimiter = ";"

    input_csv = os.path.join(tmpdir, "input.csv")
    with open(input_csv, "w", encoding="utf-8") as outfile:
        outfile.write(f"{src_header}{delimiter}{dest_header}")

        for k, v in translations.items():
            outfile.write(f"\n{k}{delimiter}{v}")

    translator = CsvTranslator(
        input_csv, src_header=src_header, dest_header=dest_header, delimiter=delimiter
    )
    assert translator._translations == translations


def test_init_detects_duplicates(tmpdir: str):
    translations = {
        "hello": "你好",
        "world": "世界",
    }

    input_csv = os.path.join(tmpdir, "input.csv")
    with open(input_csv, "w", encoding="utf-8") as outfile:
        outfile.write("source,destination")

        for k, v in translations.items():
            outfile.write(f"\n{k},{v}")

        outfile.write("\nhello,again")

    with pytest.raises(RuntimeError):
        CsvTranslator(input_csv)