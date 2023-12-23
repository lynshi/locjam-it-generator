"""Helpers for getting statistics about translations."""

from typing import Dict, List, Set, Tuple


class TranslationStatistics:
    """Accumulator for translations statistics."""

    def __init__(self, translations: Dict[str, str]):
        self._use_count = {k: 0 for k in translations.keys()}
        self._counts = {0: set(translations.keys())}

    def count_use(self, source: str) -> None:
        """Registers a use of the source string."""
        prev = self._use_count[source]
        curr = prev + 1

        self._use_count[source] = curr

        self._counts[prev].remove(source)
        if len(self._counts[prev]) == 0:
            del self._counts[prev]

        if curr not in self._counts:
            self._counts[curr] = set()

        self._counts[curr].add(source)

    def get_unused(self) -> Set[str]:
        """Gets a set of the unused words."""
        return self._counts[0]

    def get_use_counts(self) -> Dict[str, int]:
        """Returns the number of times each string has been used."""
        return self._use_count

    def get_repeatedly_used(self) -> List[Tuple[int, Set[str]]]:
        """Returns a list of translations used multiple times sorted in descending order."""
        multi_use = []
        for c in sorted(self._counts, reverse=True):
            if c in {0, 1}:
                break

            multi_use.append((c, self._counts[c]))

        return multi_use
