# locjam-it-generator
[![codecov](https://codecov.io/gh/lynshi/locjam-it-generator/graph/badge.svg?token=f3stB3Ck1S)](https://codecov.io/gh/lynshi/locjam-it-generator)

Generates a finalized JS file for LocJAM Made in Italy.

# How to use
## Prerequisites
1. Create and activate a [virtualenv](https://virtualenvwrapper.readthedocs.io/en/latest/).
2. Install requirements: `pip install -r requirements.txt`.

## Create a configuration file.
Create a file `config.json` with the following information. Currently, we only support translations in CSV files.
```json
{
  "input": "it-it.i18n.js",
  "output": "i18n.js",
  "statistics": "statistics.json",
  "translations": "NAME_OF_THE_FILE_CONTAINING_YOUR_TRANSLATIONS.csv",
  // `csv` may be omitted if you don't have any special settings.
  "csv": {
    "src_header": "HEADER_OF_ITALIAN_COLUMN",
    "dest_header": "HEADER_OF_NON_ITALIAN_COLUMN",
    "delimiter": "CSV_DELIMITER_IF_NOT_COMMA"
  }
}
```

## Usage
```bash
configFile="config.json" # Set this to the name of your configuration file.
python -c $configFile
```
