import json
import os

import pytest

from locjamit import Config


def test_init_config_not_found(tmpdir: str):
    config_file = os.path.join(tmpdir, "config.json")

    with pytest.raises(FileNotFoundError):
        Config(config_file)


def test_init(tmpdir: str):
    config_json = {
        "input": "/path/to/input.txt",
        "output": "/path/to/output.txt",
        "translations": "/path/to/translations.txt",
    }

    config_file = os.path.join(tmpdir, "config.json")
    with open(config_file, "w", encoding="utf-8") as outfile:
        json.dump(config_json, outfile)

    config = Config(config_file)
    assert config.input_file == config_json["input"]
    assert config.output_file == config_json["output"]
    assert config.translations_file == config_json["translations"]


@pytest.mark.parametrize("missing_key", ["input", "output", "translations"])
def test_init_missing_keys(tmpdir: str, missing_key: str):
    config_json = {
        "input": "/path/to/input.txt",
        "output": "/path/to/output.txt",
        "translations": "/path/to/translations.txt",
    }
    del config_json[missing_key]

    config_file = os.path.join(tmpdir, "config.json")
    with open(config_file, "w", encoding="utf-8") as outfile:
        json.dump(config_json, outfile)

    with pytest.raises(ValueError):
        Config(config_file)
