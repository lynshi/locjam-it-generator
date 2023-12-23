import os

import pytest

from locjamit.replacer import Replacer, ReplaceStatus
from locjamit.replacer._replacer import ReplaceResult


@pytest.mark.parametrize(
    "status", filter(lambda x: x is not ReplaceStatus.SUCCESS, list(ReplaceStatus))
)
def test_ReplaceResult_init_raisesIfResultProvidedAndStatusNotSuccess(
    status: ReplaceStatus,
):
    with pytest.raises(ValueError):
        ReplaceResult(status, "")

    with pytest.raises(ValueError):
        ReplaceResult(status, "anything")


def test_ReplaceResult_init_raisesIfResultNotProvidedAndStatusSuccess():
    with pytest.raises(ValueError):
        ReplaceResult(ReplaceStatus.SUCCESS, "")

    with pytest.raises(ValueError):
        ReplaceResult(ReplaceStatus.SUCCESS, None)

    with pytest.raises(ValueError):
        ReplaceResult(ReplaceStatus.SUCCESS)


@pytest.mark.parametrize(
    "status", filter(lambda x: x is not ReplaceStatus.SUCCESS, list(ReplaceStatus))
)
def test_ReplaceResult_propertiesWhenNotSuccess(status: ReplaceStatus):
    result = ReplaceResult(status)
    assert result.status is status

    with pytest.raises(RuntimeError):
        print(result.value)


def test_ReplaceResult_propertiesWhenSuccess():
    value = "Hello world"
    result = ReplaceResult(ReplaceStatus.SUCCESS, value)

    assert result.status is ReplaceStatus.SUCCESS
    assert result.value == value


def test_init_raisesIfFileNotFound(tmpdir: str):
    input_file = os.path.join(tmpdir, "notexists.txt")

    with pytest.raises(FileNotFoundError):
        Replacer(input_file, lambda _: {})


def test_init(tmpdir: str):
    input_file = os.path.join(tmpdir, "notexists.txt")
    with open(input_file, "w", encoding="utf-8") as outfile:
        outfile.write("Hello, world!")

    replacer = Replacer(input_file, lambda _: {"hello": "world"})
    assert replacer._translations == {"hello": "world"}


def test_replace_notFound(tmpdir: str):
    input_file = os.path.join(tmpdir, "notexists.txt")
    with open(input_file, "w", encoding="utf-8") as outfile:
        outfile.write("Hello, world!")

    replacer = Replacer(input_file, lambda _: {})

    assert replacer.replace("Anything").status is ReplaceStatus.NOT_FOUND


def test_replace(tmpdir: str):
    input_file = os.path.join(tmpdir, "notexists.txt")
    with open(input_file, "w", encoding="utf-8") as outfile:
        outfile.write("Hello, world!")

    replacer = Replacer(input_file, lambda _: {"hello": "world"})

    result = replacer.replace("hello")

    assert result.status is ReplaceStatus.SUCCESS
    assert result.value == "world"
