"""Helpers for getting statistics about translations."""

from typing import Dict, List


class TranslationStatistics:
    """Accumulator for translations statistics."""

    def __init__(self, translations: Dict[str, str], duplicates: List[str]):
        # Using list to preserve the order. Dictionary key order is deterministic!
        self._duplicates = duplicates
        self._unused = [translations[k] for k in translations.keys()]

    def register_use(self, dest: str) -> None:
        """Registers a use of the source string."""
        if dest in self._unused:
            self._unused = list(filter(lambda x: x != dest, self._unused))

    @property
    def duplicates(self):
        """Gets duplicated translations."""
        return self._duplicates

    @property
    def unused(self) -> List[str]:
        """Gets a list of the unused strings."""
        return self._unused
