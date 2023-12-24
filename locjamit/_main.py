"""Main method for the replacer."""

import argparse
import os

from loguru import logger

from locjamit._config import Config
from locjamit._replacer import Replacer
from locjamit.translation import CsvConfig, CsvTranslator


def main():
    parser = argparse.ArgumentParser(
        "locjamit",
        description="Generates a JavaScript file containing translated strings for LocJAM Made in Italy",
    )

    parser.add_argument(
        "-c",
        "--config",
        description="Path to the configuration file",
        required=True,
        type=str,
    )

    args = parser.parse_args()
    config_file = args.config

    logger.info("Starting program...")
    logger.debug(f"Loading configuration from {config_file}")

    config = Config(config_file)
    _, ext = os.path.splitext(config.translations_file)
    if ext == ".csv":
        csv_config = CsvConfig(config.csv_config)
        translator = CsvTranslator(config.translations_file, **csv_config.as_kwargs())
    else:
        raise RuntimeError(f"Unsupported input file type {ext}")

    logger.info(
        f"Translating {config.input_file} using {config.translations_file}. "
        f"Output will be written to {config.output_file}"
    )
    replacer = Replacer(
        input_file=config.input_file,
        output_file=config.output_file,
        translator=translator,
    )

    try:
        replacer.replace()
    except Exception:
        logger.opt(exception=True).error("Error generating translated file")
        raise

    logger.success(f"Translation success! Please open {config.output_file}")
