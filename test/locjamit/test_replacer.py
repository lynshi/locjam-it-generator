import json
import os
from unittest.mock import MagicMock

import pytest

from locjamit import ReplacementStatus, Replacer, Translator
from locjamit.translation import CsvTranslator, TranslationStatus
from locjamit.translation._translator import TranslationResult


def test_init_input_not_found(tmpdir: str, translator: Translator):
    input_file = os.path.join(tmpdir, "not-found.txt")
    statistics_file = os.path.join(tmpdir, "stats.txt")
    with pytest.raises(FileNotFoundError):
        Replacer(
            input_file=input_file,
            output_file="",
            statistics_file=statistics_file,
            translator=translator,
        )


def test_init(tmpdir: str, translator: Translator):
    input_js = "import svelte;"
    input_file = os.path.join(tmpdir, "input.txt")
    with open(input_file, "w", encoding="utf-8") as outfile:
        outfile.write(input_js)

    statistics_file = os.path.join(tmpdir, "stats.txt")
    output_file = os.path.join(tmpdir, "output.txt")

    replacer = Replacer(
        input_file=input_file,
        output_file=output_file,
        statistics_file=statistics_file,
        translator=translator,
    )

    assert replacer._original_js == input_js
    assert replacer._translator == translator
    assert replacer.output_file == output_file
    assert replacer._translated is False


def build_replacer(tmpdir: str, translator: Translator, input_js: str):
    input_file = os.path.join(tmpdir, "input.txt")
    with open(input_file, "w", encoding="utf-8") as outfile:
        outfile.write(input_js)

    statistics_file = os.path.join(tmpdir, "stats.txt")
    output_file = os.path.join(tmpdir, "output.txt")

    return Replacer(
        input_file=input_file,
        output_file=output_file,
        statistics_file=statistics_file,
        translator=translator,
    )


def test_replace(tmpdir: str, translator: Translator):
    input_js = """var i18n = {
	title: `          AVVENTURA NEL CASTELLO JS          `,
	IFEngine: {
		warnings: {
			mustBeExtended: `IFEngine deve essere esteso`,
			notFound: (filename) => `Salvataggio "${filename}" non trovato.`
		},
        menu: {
			new: `Iniziare una nuova avventura`
		}
    }
}
"""
    translations = {
        "          AVVENTURA NEL CASTELLO JS          ": "  Adventure  ",
        "IFEngine deve essere esteso": "must be extended",
        'Salvataggio "${filename}" non trovato.': 'File "${filename}" not found',
        "Iniziare una nuova avventura": "this is new",
    }

    def translate(src: str) -> TranslationResult:
        if src not in translations:
            return TranslationResult(src, TranslationStatus.NOT_FOUND)

        return TranslationResult(src, TranslationStatus.SUCCESS, translations[src])

    translator.translate = translate

    mock_stats = MagicMock()
    mock_stats.unused = []
    translator.get_stats.return_value = mock_stats  # type: ignore

    replacer = build_replacer(tmpdir, translator, input_js)

    assert replacer.replace() is ReplacementStatus.SUCCESS

    with open(replacer.output_file, encoding="utf-8") as infile:
        translated = infile.read()

    assert (
        """var i18n = {
	title: `  Adventure  `,
	IFEngine: {
		warnings: {
			mustBeExtended: `must be extended`,
			notFound: (filename) => `File \"${filename}\" not found`
		},
        menu: {
			new: `this is new`
		}
    }
}
""".strip()
        == translated.strip()
    )

    assert replacer._misses == []
    assert replacer._translated is True

    with open(replacer._statistics_file, encoding="utf-8") as infile:
        stats = json.load(infile)

    assert stats == {
        "misses": {"count": 0, "strings": []},
        "unused": {"count": 0, "strings": []},
    }

    with pytest.raises(AssertionError):
        replacer.replace()


def test_replace_with_warnings(tmpdir: str):
    input_js = """var i18n = {
	title: `          AVVENTURA NEL CASTELLO JS          `,
	IFEngine: {
		warnings: {
			mustBeExtended: `IFEngine deve essere esteso`,
			notFound: (filename) => `Salvataggio "${filename}" non trovato.`
		},
        menu: {
			choose: `Vuoi:`,
            other: `avventura`,
            dup: `avventura`,
			new: `Iniziare una nuova avventura`
		}
    }
}
"""
    translations = {
        "          AVVENTURA NEL CASTELLO JS          ": "  Adventure  ",
        "IFEngine deve essere esteso": "must be extended",
        'Salvataggio "${filename}" non trovato.': 'File "${filename}" not found',
        "Iniziare una nuova avventura": "this is new",
        "unused": "not-used",
        "utf": "喔",
    }
    translations_csv = ["source,destination"]
    for k, v in translations.items():
        translations_csv.append(f"{k},{v}")

    transations_file = os.path.join(tmpdir, "translations.csv")
    with open(transations_file, "w", encoding="utf-8") as outfile:
        outfile.write("\n".join(translations_csv))

    replacer = build_replacer(tmpdir, CsvTranslator(transations_file), input_js)

    assert replacer.replace() == ReplacementStatus.WARNING

    with open(replacer.output_file, encoding="utf-8") as infile:
        translated = infile.read()

    assert (
        """var i18n = {
	title: `  Adventure  `,
	IFEngine: {
		warnings: {
			mustBeExtended: `must be extended`,
			notFound: (filename) => `File \"${filename}\" not found`
		},
        menu: {
			choose: `Vuoi:`,
            other: `avventura`,
            dup: `avventura`,
			new: `this is new`
		}
    }
}
""".strip()
        == translated.strip()
    )

    assert replacer._misses == [
        "Vuoi:",
        "avventura",
        "avventura",
    ]
    assert replacer._translated is True

    with open(replacer._statistics_file, encoding="utf-8") as infile:
        stats = json.load(infile)

    assert stats == {
        "misses": {"count": 3, "strings": ["Vuoi:", "avventura", "avventura"]},
        "unused": {"count": 2, "strings": ["not-used", "喔"]},
    }
