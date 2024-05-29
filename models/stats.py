from beanie import Document
from dicts import (
    hiragana_basic_stats,
    hiragana_kuten_stats,
    hiragana_kuten_combinations_stats,
    katakana_basic_stats,
    katakana_kuten_stats,
    katakana_kuten_combinations_stats,
)


class Stats(Document):
    hiragana_basic: dict = hiragana_basic_stats
    hiragana_kuten: dict = hiragana_kuten_stats
    hiragana_kuten_combinations: dict = hiragana_kuten_combinations_stats
    katakana_basic: dict = katakana_basic_stats
    katakana_kuten: dict = katakana_kuten_stats
    katakana_kuten_combinations: dict = katakana_kuten_combinations_stats
