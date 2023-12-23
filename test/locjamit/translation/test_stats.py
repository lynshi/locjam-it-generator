from locjamit.translation import TranslationStatistics


def test_init():
    translations = {"hello": "0", "world": "1"}
    stats = TranslationStatistics(translations)

    assert stats._use_count == {
        "hello": 0,
        "world": 0,
    }

    assert stats._counts == {0: {"hello", "world"}}


def test_count_use():
    translations = {"hello": "0", "world": "1"}
    stats = TranslationStatistics(translations)

    stats.count_use("hello")
    assert stats._use_count == {
        "hello": 1,
        "world": 0,
    }
    assert stats._counts == {0: {"world"}, 1: {"hello"}}

    stats.count_use("hello")
    assert stats._use_count == {
        "hello": 2,
        "world": 0,
    }
    assert stats._counts == {0: {"world"}, 2: {"hello"}}


def test_get_unused():
    translations = {"hello": "0", "world": "1"}
    stats = TranslationStatistics(translations)

    stats.count_use("hello")
    assert stats.get_unused() == {"world"}


def test_get_use_counts():
    translations = {"hello": "0", "world": "1"}
    stats = TranslationStatistics(translations)

    stats.count_use("hello")
    assert stats.get_use_counts() == {
        "hello": 1,
        "world": 0,
    }


def test_get_repeatedly_used():
    translations = {"hello": "0", "world": "1", "!": "2", "once": "3", "twice": "4"}
    stats = TranslationStatistics(translations)

    stats.count_use("hello")
    stats.count_use("hello")
    stats.count_use("!")
    stats.count_use("!")
    stats.count_use("!")
    stats.count_use("once")
    stats.count_use("twice")
    stats.count_use("twice")
    assert stats.get_repeatedly_used() == [(3, {"!"}), (2, {"hello", "twice"})]


def test_get_repeatedly_used_ignores_once():
    translations = {"hello": "0", "!": "2", "once": "3", "twice": "4"}
    stats = TranslationStatistics(translations)

    stats.count_use("hello")
    stats.count_use("hello")
    stats.count_use("!")
    stats.count_use("!")
    stats.count_use("!")
    stats.count_use("once")
    stats.count_use("twice")
    stats.count_use("twice")
    assert stats.get_repeatedly_used() == [(3, {"!"}), (2, {"hello", "twice"})]


def test_get_repeatedly_used_ignores_zero():
    translations = {"hello": "0", "world": "1", "!": "2", "twice": "4"}
    stats = TranslationStatistics(translations)

    stats.count_use("hello")
    stats.count_use("hello")
    stats.count_use("!")
    stats.count_use("!")
    stats.count_use("!")
    stats.count_use("twice")
    stats.count_use("twice")
    assert stats.get_repeatedly_used() == [(3, {"!"}), (2, {"hello", "twice"})]


def test_get_repeatedly_used_all_repeated():
    translations = {"hello": "0", "!": "2", "twice": "4"}
    stats = TranslationStatistics(translations)

    stats.count_use("hello")
    stats.count_use("hello")
    stats.count_use("!")
    stats.count_use("!")
    stats.count_use("!")
    stats.count_use("twice")
    stats.count_use("twice")
    assert stats.get_repeatedly_used() == [(3, {"!"}), (2, {"hello", "twice"})]
