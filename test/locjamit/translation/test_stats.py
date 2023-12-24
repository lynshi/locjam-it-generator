from locjamit.translation import TranslationStatistics


def test_init():
    translations = {"hello": "1", "world": "0"}
    stats = TranslationStatistics(translations)

    assert stats._unused == ["1", "0"]


def test_register_use():
    translations = {"hello": "0", "world": "1"}
    stats = TranslationStatistics(translations)

    stats.register_use("0")
    assert stats.unused == ["1"]

    stats.register_use("0")
    assert stats.unused == ["1"]
