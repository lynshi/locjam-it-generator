import os

import pytest

from locjamit.translation import Translator, TranslationStatus
from locjamit.translation._translator import TranslationResult


@pytest.mark.parametrize(
    "status",
    filter(lambda x: x is not TranslationStatus.SUCCESS, list(TranslationStatus)),
)
def test_TranslationResult_init_raises_if_result_provided_unexpectedly(
    status: TranslationStatus,
):
    with pytest.raises(ValueError):
        TranslationResult("src", status, "")

    with pytest.raises(ValueError):
        TranslationResult("src", status, "anything")


def test_TranslationResult_init_raises_if_result_not_provided():
    with pytest.raises(ValueError):
        TranslationResult("src", TranslationStatus.SUCCESS, "")

    with pytest.raises(ValueError):
        TranslationResult("src", TranslationStatus.SUCCESS, None)

    with pytest.raises(ValueError):
        TranslationResult("src", TranslationStatus.SUCCESS)


@pytest.mark.parametrize(
    "status",
    filter(lambda x: x is not TranslationStatus.SUCCESS, list(TranslationStatus)),
)
def test_TranslationResult_properties_when_not_success(status: TranslationStatus):
    result = TranslationResult("src", status)
    assert result.status is status

    with pytest.raises(RuntimeError):
        print(result.value)


def test_TranslationResult_properties_when_success():
    src = "src"
    value = "Hello world"
    result = TranslationResult(src, TranslationStatus.SUCCESS, value)

    assert result.status is TranslationStatus.SUCCESS
    assert result.source == src
    assert result.value == value


def test_init_raises_if_file_not_found(tmpdir: str):
    input_file = os.path.join(tmpdir, "notexists.txt")

    with pytest.raises(FileNotFoundError):
        Translator(input_file, lambda _: {})


def test_init(tmpdir: str):
    input_file = os.path.join(tmpdir, "notexists.txt")
    with open(input_file, "w", encoding="utf-8") as outfile:
        outfile.write("Hello, world!")

    translator = Translator(input_file, lambda _: {"hello": "world"})
    assert translator._translations == {"hello": "world"}


def test_translate_not_found(tmpdir: str):
    input_file = os.path.join(tmpdir, "notexists.txt")
    with open(input_file, "w", encoding="utf-8") as outfile:
        outfile.write("Hello, world!")

    translator = Translator(input_file, lambda _: {})

    assert translator.translate("Anything").status is TranslationStatus.NOT_FOUND


def test_translate(tmpdir: str):
    input_file = os.path.join(tmpdir, "notexists.txt")
    with open(input_file, "w", encoding="utf-8") as outfile:
        outfile.write("Hello, world!")

    translator = Translator(input_file, lambda _: {"hello": "world"})

    result = translator.translate("hello")

    assert result.status is TranslationStatus.SUCCESS
    assert result.value == "world"