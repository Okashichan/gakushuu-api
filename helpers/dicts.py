import re
import deepl
from jamdict import Jamdict
import pykakasi
from config import settings


def hiragana_to_katakana(text):
    katakana_text = []

    for char in text:
        code_point = ord(char)

        if 0x3041 <= code_point <= 0x3096:
            katakana_char = chr(code_point + 0x60)
            katakana_text.append(katakana_char)
        else:
            katakana_text.append(char)

    return ''.join(katakana_text)


def get_kanji_info(query: str | int, deeplapi: bool = False):
    jam = Jamdict()
    kks = pykakasi.kakasi()

    results = []

    kanji_info = jam.lookup(query) if isinstance(
        query, str) else jam.lookup(f'id#{query}')

    if not kanji_info:
        return "Kanji not found in the dictionary."

    for index, entry in enumerate(kanji_info.entries):
        hiragana = entry.kana_forms[0].text
        results.append({
            "idseq": entry.idseq,
            "kanji": entry.kanji_forms[0].text if len(entry.kanji_forms) > 0 else None,
            "hiragana": hiragana,
            "katakana": entry.kana_forms[-1].text if (len(entry.kana_forms) > 1 and bool(re.match(r'^[\u30A0-\u30FF]+$', entry.kana_forms[-1].text))) else None,
            "romaji": kks.convert(hiragana)[0]['hepburn'],
            "transliteration": hiragana_to_ukrainian(hiragana),
            "kunyomi": kanji_info.chars[0].rm_groups[0].kun_readings[0].value if len(kanji_info.chars) > 0 and len(kanji_info.chars[0].rm_groups[0].kun_readings) > 0 else None,
            "onyomi": kanji_info.chars[0].rm_groups[0].on_readings[0].value if len(kanji_info.chars) > 0 and len(kanji_info.chars[0].rm_groups[0].on_readings) > 0 else None,
            "en_translation": entry.senses[0].gloss[0].text,
            "ua_translation": None,
        })

    if deeplapi:
        translator = deepl.Translator(settings.DEEPL_API_KEY)
        results[0]["ua_translation"] = translator.translate_text(
            results[0]["en_translation"], source_lang='EN', target_lang='UK').text

        if results[0]['katakana'] is None:
            results[0]['katakana'] = hiragana_to_katakana(
                results[0]['hiragana'])

    return results


def hiragana_to_ukrainian(query, info=False):
    kks = pykakasi.kakasi()
    force_hira = ''.join([f['hira'] for f in kks.convert(query)])
    htudict = hiragana_full
    ukrainian_text = ""
    i = 0
    while i < len(force_hira):
        if i + 1 < len(force_hira) and force_hira[i:i+2] in htudict:
            ukrainian_text += htudict[force_hira[i:i+2]]
            i += 2
        else:
            ukrainian_text += htudict.get(force_hira[i], force_hira[i])
            i += 1
    if info:
        return {
            "ukrainian": ukrainian_text,
            "hiragana": force_hira,
            "romaji": ''.join([f['hepburn'] for f in kks.convert(query)]),
        }
    return ukrainian_text


# Hiragana
hiragana_basic = {
    "あ": "а", "い": "і", "う": "у", "え": "е", "お": "о",
    "か": "ка", "き": "кі", "く": "ку", "け": "ке", "こ": "ко",
    "さ": "са", "し": "ші", "す": "су", "せ": "се", "そ": "со",
    "た": "та", "ち": "чі", "つ": "цу", "て": "те", "と": "то",
    "な": "на", "に": "ні", "ぬ": "ну", "ね": "не", "の": "но",
    "は": "ха", "ひ": "хі", "ふ": "фу", "へ": "хе", "ほ": "хо",
    "ま": "ма", "み": "мі", "む": "му", "め": "ме", "も": "мо",
    "や": "я", "ゆ": "ю", "よ": "йо",
    "ら": "ра", "り": "рі", "る": "ру", "れ": "ре", "ろ": "ро",
    "わ": "ва", "を": "о", "ん": "н",
}

hiragana_combinations = {
    "きゃ": "кя", "きゅ": "кю", "きょ": "кьо",
    "しゃ": "шя", "しゅ": "шю", "しょ": "шьо",
    "ちゃ": "чя", "ちゅ": "чю", "ちょ": "чьо",
    "にゃ": "ня", "にゅ": "ню", "にょ": "ньо",
    "ひゃ": "хя", "ひゅ": "хю", "ひょ": "хьо",
    "みゃ": "мя", "みゅ": "мю", "みょ": "мьо",
    "りゃ": "ря", "りゅ": "рю", "りょ": "рьо",
}

hiragana_kuten = {
    "が": "ґа", "ぎ": "ґі", "ぐ": "ґу", "げ": "ґе", "ご": "ґо",
    "ざ": "дза", "じ": "джі", "ず": "дзу", "ぜ": "дзе", "ぞ": "дзо",
    "だ": "да", "ぢ": "джі", "づ": "дзу", "で": "де", "ど": "до",
    "ば": "ба", "び": "бі", "ぶ": "бу", "べ": "бе", "ぼ": "бо",
    "ぱ": "па", "ぴ": "пі", "ぷ": "пу", "ぺ": "пе", "ぽ": "по",
}


hiragana_kuten_combinations = {
    "ぎゃ": "ґя", "ぎゅ": "ґю", "ぎょ": "ґьо",
    "じゃ": "джя", "じゅ": "джю", "じょ": "джьо",
    "ぢゃ": "джя", "ぢゅ": "джю", "ぢょ": "джьо",
    "びゃ": "бя", "びゅ": "бю", "びょ": "бьо",
    "ぴゃ": "пя", "ぴゅ": "пю", "ぴょ": "пьо",
}

hiragana_full = {**hiragana_basic, **hiragana_combinations,
                 **hiragana_kuten, **hiragana_kuten_combinations}

hiragana_basic_stats = {k[0]: {"right": 0, "wrong": 0}
                        for k in hiragana_basic.items()}

hiragana_kuten_stats = {k[0]: {"right": 0, "wrong": 0}
                        for k in hiragana_kuten.items()}

hiragana_kuten_combinations_stats = {k[0]: {"right": 0, "wrong": 0}
                                     for k in {**hiragana_combinations, **hiragana_kuten_combinations}.items()}


# Katakana
katakana_basic = {
    "ア": "а", "イ": "і", "ウ": "у", "エ": "е", "オ": "о",
    "カ": "ка", "キ": "кі", "ク": "ку", "ケ": "ке", "コ": "ко",
    "サ": "са", "シ": "ші", "ス": "су", "セ": "се", "ソ": "со",
    "タ": "та", "チ": "чі", "ツ": "цу", "テ": "те", "ト": "то",
    "ナ": "на", "ニ": "ні", "ヌ": "ну", "ネ": "не", "ノ": "но",
    "ハ": "ха", "ヒ": "хі", "フ": "фу", "ヘ": "хе", "ホ": "хо",
    "マ": "ма", "ミ": "мі", "ム": "му", "メ": "ме", "モ": "мо",
    "ヤ": "я", "ユ": "ю", "ヨ": "йо",
    "ラ": "ра", "リ": "рі", "ル": "ру", "レ": "ре", "ロ": "ро",
    "ワ": "ва", "ヲ": "о", "ン": "н",
}

katakana_combinations = {
    "キャ": "кя", "キュ": "кю", "キョ": "кьо",
    "シャ": "шя", "シュ": "шю", "ショ": "шьо",
    "チャ": "чя", "チュ": "чю", "チョ": "чьо",
    "ニャ": "ня", "ニュ": "ню", "ニョ": "ньо",
    "ヒャ": "хя", "ヒュ": "хю", "ヒョ": "хьо",
    "ミャ": "мя", "ミュ": "мю", "ミョ": "мьо",
    "リャ": "ря", "リュ": "рю", "リョ": "рьо",
}

katakana_kuten = {
    "ガ": "ґа", "ギ": "ґі", "グ": "ґу", "ゲ": "ґе", "ゴ": "ґо",
    "ザ": "дза", "ジ": "джі", "ズ": "дзу", "ゼ": "дзе", "ゾ": "дзо",
    "ダ": "да", "ヂ": "джі", "ヅ": "дзу", "デ": "де", "ド": "до",
    "バ": "ба", "ビ": "бі", "ブ": "бу", "ベ": "бе", "ボ": "бо",
    "パ": "па", "ピ": "пі", "プ": "пу", "ペ": "пе", "ポ": "по",
}

katakana_kuten_combinations = {
    "ギャ": "ґя", "ギュ": "ґю", "ギョ": "ґьо",
    "ジャ": "джя", "ジュ": "джю", "ジョ": "джьо",
    "ヂャ": "джя", "ヂュ": "джю", "ヂョ": "джьо",
    "ビャ": "бя", "ビュ": "бю", "ビョ": "бьо",
    "ピャ": "пя", "ピュ": "пю", "ピョ": "пьо",
}

katakana_full = {**katakana_basic, **katakana_combinations,
                 **katakana_kuten, **katakana_kuten_combinations}

katakana_stats = {k[0]: {"right": 0, "wrong": 0}
                  for k in katakana_full.items()}

katakana_basic_stats = {k[0]: {"right": 0, "wrong": 0}
                        for k in katakana_basic.items()}

katakana_kuten_stats = {k[0]: {"right": 0, "wrong": 0}
                        for k in katakana_kuten.items()}

katakana_kuten_combinations_stats = {k[0]: {"right": 0, "wrong": 0}
                                     for k in {**katakana_combinations, **katakana_kuten_combinations}.items()}
