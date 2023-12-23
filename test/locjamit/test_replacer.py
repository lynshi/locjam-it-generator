import os

import pytest

from locjamit import Replacer, Translator


def test_init_input_not_found(tmpdir: str, translator: Translator):
    input_file = os.path.join(tmpdir, "not-found.txt")
    with pytest.raises(FileNotFoundError):
        Replacer(input_file=input_file, output_file="", translator=translator)


def test_init_raises_if_output_exists(tmpdir: str, translator: Translator):
    input_file = os.path.join(tmpdir, "input.txt")
    with open(input_file, "w", encoding="utf-8"):
        pass

    output_file = os.path.join(tmpdir, "output.txt")
    with open(output_file, "w", encoding="utf-8"):
        pass

    with pytest.raises(FileExistsError):
        Replacer(input_file=input_file, output_file=output_file, translator=translator)


def test_init(tmpdir: str, translator: Translator):
    input_js = "import svelte;"
    input_file = os.path.join(tmpdir, "input.txt")
    with open(input_file, "w", encoding="utf-8") as outfile:
        outfile.write(input_js)

    output_file = os.path.join(tmpdir, "output.txt")

    replacer = Replacer(
        input_file=input_file, output_file=output_file, translator=translator
    )

    assert replacer._original_js == input_js
    assert replacer._translator == translator
    assert replacer._output_file == output_file


def test_init_exists_ok(tmpdir: str, translator: Translator):
    input_js = "import svelte;"
    input_file = os.path.join(tmpdir, "input.txt")
    with open(input_file, "w", encoding="utf-8") as outfile:
        outfile.write(input_js)

    output_file = os.path.join(tmpdir, "output.txt")
    with open(output_file, "w", encoding="utf-8"):
        pass

    replacer = Replacer(
        input_file=input_file,
        output_file=output_file,
        translator=translator,
        overwrite_output=True,
    )

    assert replacer._original_js == input_js
    assert replacer._translator == translator
    assert replacer._output_file == output_file


def build_replacer(tmpdir: str, translator: Translator, input_js: str):
    input_file = os.path.join(tmpdir, "input.txt")
    with open(input_file, "w", encoding="utf-8") as outfile:
        outfile.write(input_js)

    output_file = os.path.join(tmpdir, "output.txt")

    return Replacer(
        input_file=input_file,
        output_file=output_file,
        translator=translator,
        overwrite_output=True,
    )


def test_replace(tmpdir: str, translator: Translator):
    input_js = """"""
    replacer = build_replacer(tmpdir, translator, input_js)

    replacer.replace()
