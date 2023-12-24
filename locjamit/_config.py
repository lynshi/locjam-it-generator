"""Configuration for the program."""

import json
import os

from loguru import logger


class Config:
    def __init__(self, config_file: str):
        if not os.path.isfile(config_file):
            raise FileNotFoundError(f"{config_file} not found")

        with open(config_file, encoding="utf-8") as infile:
            self._config = json.load(infile)

        logger.debug(
            f"""Parameters:\n
            \tInput file: {self.input_file}\n
            \tOutput file: {self.output_file}\n
            \tTranslations file: {self.translations_file}\n"""
        )

    @property
    def input_file(self) -> str:
        field_name = "input"
        try:
            return self._config[field_name]
        except KeyError:
            raise ValueError(f"`{field_name}` field not present in configuration")

    @property
    def output_file(self) -> str:
        field_name = "output"
        try:
            return self._config[field_name]
        except KeyError:
            raise ValueError(f"`{field_name}` field not present in configuration")

    @property
    def translations_file(self) -> str:
        field_name = "translations"
        try:
            return self._config[field_name]
        except KeyError:
            raise ValueError(f"`{field_name}` field not present in configuration")
