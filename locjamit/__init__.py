"""`locjamit` is a utility for generating a translated JavaScript file for the Avventura nel
Castello game that is the subject of LocJAM Made in Italy: https://itch.io/jam/locjam-it
"""

from locjamit import translation
from locjamit.translation import CsvTranslator, Translator
from locjamit._config import Config
from locjamit._main import main
from locjamit._replacer import ReplacementStatus, Replacer
