"""Configuration for the program."""

import json
import os
from typing import Any, Dict


class Config:
    """Loads configuration for the program."""

    def __init__(self, config_file: str):
        if not os.path.isfile(config_file):
            raise FileNotFoundError(f"{config_file} not found")

        with open(config_file, encoding="utf-8") as infile:
            self._config = json.load(infile)

    @property
    def csv_config(  # pylint: disable=missing-function-docstring
        self,
    ) -> Dict[str, Any]:
        return self._config.get("csv", {})

    @property
    def input_file(self) -> str:  # pylint: disable=missing-function-docstring
        field_name = "input"
        return self._get_field(field_name)

    @property
    def output_file(self) -> str:  # pylint: disable=missing-function-docstring
        field_name = "output"
        return self._get_field(field_name)

    @property
    def stats_file(self) -> str:  # pylint: disable=missing-function-docstring
        field_name = "statistics"
        return self._get_field(field_name)

    @property
    def translations_file(self) -> str:  # pylint: disable=missing-function-docstring
        field_name = "translations"
        return self._get_field(field_name)

    def _get_field(self, field_name: str) -> Any:
        try:
            return self._config[field_name]
        except KeyError as exc:
            raise ValueError(
                f"`{field_name}` field not present in configuration"
            ) from exc
