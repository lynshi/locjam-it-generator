import os

import pytest

from locjamit.translation import Translator, TranslationStatus
from locjamit.translation._translator import TranslationResult


@pytest.mark.parametrize(
    "status",
    filter(lambda x: x is not TranslationStatus.SUCCESS, list(TranslationStatus)),
)
def test_TranslationResult_init_raisesIfResultProvidedAndStatusNotSuccess(
    status: TranslationStatus,
):
    with pytest.raises(ValueError):
        TranslationResult(status, "")

    with pytest.raises(ValueError):
        TranslationResult(status, "anything")


def test_TranslationResult_init_raisesIfResultNotProvidedAndStatusSuccess():
    with pytest.raises(ValueError):
        TranslationResult(TranslationStatus.SUCCESS, "")

    with pytest.raises(ValueError):
        TranslationResult(TranslationStatus.SUCCESS, None)

    with pytest.raises(ValueError):
        TranslationResult(TranslationStatus.SUCCESS)


@pytest.mark.parametrize(
    "status",
    filter(lambda x: x is not TranslationStatus.SUCCESS, list(TranslationStatus)),
)
def test_TranslationResult_propertiesWhenNotSuccess(status: TranslationStatus):
    result = TranslationResult(status)
    assert result.status is status

    with pytest.raises(RuntimeError):
        print(result.value)


def test_TranslationResult_propertiesWhenSuccess():
    value = "Hello world"
    result = TranslationResult(TranslationStatus.SUCCESS, value)

    assert result.status is TranslationStatus.SUCCESS
    assert result.value == value


def test_init_raisesIfFileNotFound(tmpdir: str):
    input_file = os.path.join(tmpdir, "notexists.txt")

    with pytest.raises(FileNotFoundError):
        Translator(input_file, lambda _: {})


def test_init(tmpdir: str):
    input_file = os.path.join(tmpdir, "notexists.txt")
    with open(input_file, "w", encoding="utf-8") as outfile:
        outfile.write("Hello, world!")

    translator = Translator(input_file, lambda _: {"hello": "world"})
    assert translator._translations == {"hello": "world"}


def test_translate_notFound(tmpdir: str):
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
