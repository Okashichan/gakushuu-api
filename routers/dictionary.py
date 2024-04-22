from typing import List
from uuid import UUID
from beanie import PydanticObjectId
from beanie.odm.operators.find.logical import Or
from fastapi import APIRouter, Depends, HTTPException, Request, status
import pykakasi
from jamdict import Jamdict
from auth.oauth2 import get_current_user

from schemas.dictionary import (DictionaryBase, DictionaryMassSearch)
from models.user import User
from models.dictionary import Dictionary


router = APIRouter(
    prefix="/dictionary",
    tags=["Dictionary"]
)


def get_kanji_info(query: str | int):

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
            "kanji": entry.kanji_forms[0].text if len(entry.kanji_forms) > 1 else None,
            "hiragana": hiragana,
            "katakana": entry.kana_forms[1].text if len(entry.kana_forms) > 1 else None,
            "romaji": kks.convert(hiragana)[0]['hepburn'],
            "transliteration": hiragana_to_ukrainian(hiragana),
            "kunyomi": kanji_info.chars[0].rm_groups[0].kun_readings[0].value,
            "onyomi": kanji_info.chars[0].rm_groups[0].on_readings[0].value,
            "en_translation": entry.senses[0].gloss[0].text,
            "ua_translation": None,
        })

    return results


def hiragana_to_ukrainian(hira):
    htudict = {
        # Basic
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
        # Basic dakuten & handakuten
        "が": "ґа", "ぎ": "ґі", "ぐ": "ґу", "げ": "ґе", "ご": "ґо",
        "ざ": "дза", "じ": "джі", "ず": "дзу", "ぜ": "дзе", "ぞ": "дзо",
        "だ": "да", "ぢ": "джі", "づ": "дзу", "で": "де", "ど": "до",
        "ば": "ба", "び": "бі", "ぶ": "бу", "べ": "бе", "ぼ": "бо",
        "ぱ": "па", "ぴ": "пі", "ぷ": "пу", "ぺ": "пе", "ぽ": "по",
        # Combinations
        "きゃ": "кя", "きゅ": "кю", "きょ": "кьо",
        "しゃ": "шя", "しゅ": "шю", "しょ": "шьо",
        "ちゃ": "чя", "ちゅ": "чю", "ちょ": "чьо",
        "にゃ": "ня", "にゅ": "ню", "にょ": "ньо",
        "ひゃ": "хя", "ひゅ": "хю", "ひょ": "хьо",
        "みゃ": "мя", "みゅ": "мю", "みょ": "мьо",
        "りゃ": "ря", "りゅ": "рю", "りょ": "рьо",
        # Combinations with dakuten & handakuten
        "ぎゃ": "ґя", "ぎゅ": "ґю", "ぎょ": "ґьо",
        "じゃ": "джя", "じゅ": "джю", "じょ": "дьжо",
        "ぢゃ": "джя", "ぢゅ": "джю", "ぢょ": "дьжо",
        "びゃ": "бя", "びゅ": "бю", "びょ": "бьо",
        "ぴゃ": "пя", "ぴゅ": "пю", "ぴょ": "пьо",
    }
    ukrainian_text = ""
    i = 0
    while i < len(hira):
        if i + 1 < len(hira) and hira[i:i+2] in htudict:
            ukrainian_text += htudict[hira[i:i+2]]
            i += 2
        else:
            ukrainian_text += htudict.get(hira[i], hira[i])
            i += 1
    return ukrainian_text


@router.post("/")
async def create_entry(request: DictionaryBase, current_user: User = Depends(get_current_user)):
    dictionary = Dictionary(
        idseq=request.idseq,
        kanji=request.kanji,
        hiragana=request.hiragana,
        katakana=request.katakana,
        romaji=request.romaji,
        transliteration=request.transliteration,
        kunyomi=request.kunyomi,
        onyomi=request.onyomi,
        en_translation=request.en_translation,
        ua_translation=request.ua_translation,
        created_by=current_user.id
    )

    print(dictionary.model_dump_json())

    try:
        await dictionary.save()
        return dictionary
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Error: {e}"
        )


# @router.put("/{dictionary_id}")
# def update(dictionary_id: int, request: DictionaryUpdate, db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
#     return db_dictionary.update(db, request, dictionary_id)


# @router.delete("/{dictionary_id}")
# def delete(dictionary_id: int, db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
#     return db_dictionary.delete(db, dictionary_id)


@router.get("/id/{id}", response_model=DictionaryBase)
async def get_entry_by_id(id: PydanticObjectId):
    try:
        dic = await Dictionary.get(id)
        return dic
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Error: {e}"
        )


@router.get("/idseq/{idseq}", response_model=DictionaryBase)
async def get_entry_by_idseq(idseq: int):
    try:
        dic = await Dictionary.find_one(Dictionary.idseq == idseq)
        return dic
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Error: {e}"
        )


@router.get("/all", response_model=List[DictionaryBase])
async def get_all_entries():
    try:
        dic = await Dictionary.find_all().to_list()
        return dic
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Error: {e}"
        )


@router.get("/search/{query}", response_model=DictionaryMassSearch)
async def search(query: str):

    dic = await Dictionary.find_many(Or(Dictionary.kanji == query,
                                     Dictionary.hiragana == query,
                                     Dictionary.ua_translation == query)).to_list()
    dic_base_list = [DictionaryBase(**d.model_dump()) for d in dic]
    local = get_kanji_info(query)

    results = DictionaryMassSearch(en_sourse=local, ua_sourse=dic_base_list)

    # print(results.model_dump_json())

    return results


@router.get("/jamdict/{idseq}")
def get_jamdict(idseq: int):

    result = get_kanji_info(idseq)[0]

    return result
