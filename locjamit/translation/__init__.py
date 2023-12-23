"""Translators are objects that parse an input translation file to return translations when
requested.
"""

from locjamit.translation._csv import CsvTranslator
from locjamit.translation._translator import Translator, TranslationStatus
