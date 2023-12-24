from locjamit.translation import TranslationStatistics


def test_init():
    translations = {"hello": "0", "world": "1"}
    stats = TranslationStatistics(translations)

    assert stats._use_count == {
        "0": 0,
        "1": 0,
    }

    assert stats._counts == {0: {"0", "1"}}


def test_count_use():
    translations = {"hello": "0", "world": "1"}
    stats = TranslationStatistics(translations)

    stats.count_use("0")
    assert stats._use_count == {
        "0": 1,
        "1": 0,
    }
    assert stats._counts == {0: {"1"}, 1: {"0"}}

    stats.count_use("0")
    assert stats._use_count == {
        "0": 2,
        "1": 0,
    }
    assert stats._counts == {0: {"1"}, 2: {"0"}}


def test_get_unused():
    translations = {"hello": "0", "world": "1"}
    stats = TranslationStatistics(translations)

    stats.count_use("0")
    assert stats.get_unused() == {"1"}


def test_get_use_counts():
    translations = {"hello": "0", "world": "1"}
    stats = TranslationStatistics(translations)

    stats.count_use("0")
    assert stats.get_use_counts() == {
        "0": 1,
        "1": 0,
    }


def test_get_repeatedly_used():
    translations = {"hello": "0", "world": "1", "!": "2", "once": "3", "twice": "4"}
    stats = TranslationStatistics(translations)

    stats.count_use("0")
    stats.count_use("0")
    stats.count_use("2")
    stats.count_use("2")
    stats.count_use("2")
    stats.count_use("3")
    stats.count_use("4")
    stats.count_use("4")
    assert stats.get_repeatedly_used() == [(3, {"2"}), (2, {"0", "4"})]


def test_get_repeatedly_used_ignores_once():
    translations = {"hello": "0", "!": "2", "once": "3", "twice": "4"}
    stats = TranslationStatistics(translations)

    stats.count_use("0")
    stats.count_use("0")
    stats.count_use("2")
    stats.count_use("2")
    stats.count_use("2")
    stats.count_use("3")
    stats.count_use("4")
    stats.count_use("4")
    assert stats.get_repeatedly_used() == [(3, {"2"}), (2, {"0", "4"})]


def test_get_repeatedly_used_ignores_zero():
    translations = {"hello": "0", "world": "1", "!": "2", "twice": "4"}
    stats = TranslationStatistics(translations)

    stats.count_use("0")
    stats.count_use("0")
    stats.count_use("2")
    stats.count_use("2")
    stats.count_use("2")
    stats.count_use("4")
    stats.count_use("4")
    assert stats.get_repeatedly_used() == [(3, {"2"}), (2, {"0", "4"})]


def test_get_repeatedly_used_all_repeated():
    translations = {"hello": "0", "!": "2", "twice": "4"}
    stats = TranslationStatistics(translations)

    stats.count_use("0")
    stats.count_use("0")
    stats.count_use("2")
    stats.count_use("2")
    stats.count_use("2")
    stats.count_use("4")
    stats.count_use("4")
    assert stats.get_repeatedly_used() == [(3, {"2"}), (2, {"0", "4"})]
