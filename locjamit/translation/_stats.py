"""Helpers for getting statistics about translations."""

from typing import Dict, List


class TranslationStatistics:
    """Accumulator for translations statistics."""

    def __init__(self, translations: Dict[str, str]):
        # Using list to preserve the order. Dictionary key order is deterministic!
        self._unused = [translations[k] for k in translations.keys()]

    def register_use(self, dest: str) -> None:
        """Registers a use of the source string."""
        if dest in self._unused:
            self._unused = list(filter(lambda x: x != dest, self._unused))

    @property
    def unused(self) -> List[str]:
        """Gets a list of the unused strings."""
        return self._unused
