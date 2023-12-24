from locjamit.translation import TranslationStatistics


def test_init():
    translations = {"hello": "1", "world": "0"}
    duplicates = ["dup0", "dup1"]
    stats = TranslationStatistics(translations, duplicates)

    assert stats.duplicates == duplicates
    assert stats.unused == ["1", "0"]


def test_register_use():
    translations = {"hello": "0", "world": "1"}
    duplicates = ["dup0", "dup1"]
    stats = TranslationStatistics(translations, duplicates)

    stats.register_use("0")
    assert stats.unused == ["1"]

    stats.register_use("0")
    assert stats.unused == ["1"]
