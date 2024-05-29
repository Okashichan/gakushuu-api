from pydantic import BaseModel


class Stats(BaseModel):
    hiragana_basic: dict
    hiragana_kuten: dict
    hiragana_kuten_combinations: dict
    katakana_basic: dict
    katakana_kuten: dict
    katakana_kuten_combinations: dict
