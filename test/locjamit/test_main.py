import json
import os
import sys

import pytest

from locjamit import main


def test_unsupported_extension(tmpdir: str):
    config = {
        "input": "input.js",
        "output": "output.js",
        "statistics": "statistics.json",
        "translations": "translations.js",
    }

    config_file = os.path.join(tmpdir, "config.json")
    with open(config_file, "w", encoding="utf-8") as outfile:
        json.dump(config, outfile)

    sys.argv = ["main.py", "-c", config_file]

    with pytest.raises(RuntimeError):
        main()


def test_csv(tmpdir: str):
    config = {
        "input": os.path.join(tmpdir, "input.js"),
        "output": os.path.join(tmpdir, "output.js"),
        "statistics": os.path.join(tmpdir, "statistics.json"),
        "translations": os.path.join(tmpdir, "translations.csv"),
    }

    config_file = os.path.join(tmpdir, "config.json")
    with open(config_file, "w", encoding="utf-8") as outfile:
        json.dump(config, outfile)

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
    with open(config["input"], "w", encoding="utf-8") as outfile:
        outfile.write(input_js)

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
    translations_csv.append("utf,哇")

    with open(config["translations"], "w", encoding="utf-8") as outfile:
        outfile.write("\n".join(translations_csv))

    sys.argv = ["main.py", "-c", config_file]
    main()

    with open(config["output"], encoding="utf-8") as infile:
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

    with open(config["statistics"], encoding="utf-8") as infile:
        stats = json.load(infile)

    assert stats == {
        "misses": {"count": 3, "strings": ["Vuoi:", "avventura", "avventura"]},
        "unused": {"count": 1, "strings": ["not-used"]},
        "duplicated_translations": {
            "count": 1,
            "strings": ["utf"],
        },
    }
