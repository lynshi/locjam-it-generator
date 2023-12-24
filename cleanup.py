"""Utility script for cleaning up a CSV export."""

import csv

with open("LocJAM - strings.csv", encoding="utf-8") as infile:
    reader = csv.DictReader(infile)

    with open("translations.csv", "w", newline="") as csvfile:
        fieldnames = ["it", "zh_tw"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            tw = row["zh_tw"]

            if tw.startswith("「") and tw.endswith("」"):
                tw = tw[1:-1]

            writer.writerow({"it": row["it"][1:-1], "zh_tw": tw})
