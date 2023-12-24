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
        "input": "/path/to/input.js",
        "missed": "/path/to/missed.txt",
        "output": "/path/to/output.js",
        "translations": "/path/to/translations.csv",
    }

    config_file = os.path.join(tmpdir, "config.json")
    with open(config_file, "w", encoding="utf-8") as outfile:
        json.dump(config_json, outfile)

    config = Config(config_file)
    assert config.input_file == config_json["input"]
    assert config.missed_file == config_json["missed"]
    assert config.output_file == config_json["output"]
    assert config.translations_file == config_json["translations"]
    assert config.csv_config == {}


@pytest.mark.parametrize("missing_key", ["input", "missed", "output", "translations"])
def test_init_missing_keys(tmpdir: str, missing_key: str):
    config_json = {
        "input": "/path/to/input.js",
        "missed": "/path/to/missed.txt",
        "output": "/path/to/output.js",
        "translations": "/path/to/translations.csv",
    }
    del config_json[missing_key]

    config_file = os.path.join(tmpdir, "config.json")
    with open(config_file, "w", encoding="utf-8") as outfile:
        json.dump(config_json, outfile)

    config = Config(config_file)
    with pytest.raises(ValueError):
        assert config.input_file == config_json["input"]
        assert config.missed_file == config_json["missed"]
        assert config.output_file == config_json["output"]
        assert config.translations_file == config_json["translations"]
        assert config.csv_config == {}


def test_csv_config(tmpdir: str):
    config_json = {
        "input": "/path/to/input.js",
        "missed": "/path/to/missed.txt",
        "output": "/path/to/output.js",
        "translations": "/path/to/translations.csv",
        "csv": {
            "hello": "world",
        },
    }

    config_file = os.path.join(tmpdir, "config.json")
    with open(config_file, "w", encoding="utf-8") as outfile:
        json.dump(config_json, outfile)

    config = Config(config_file)
    assert config.csv_config == {"hello": "world"}
