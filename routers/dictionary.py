from datetime import datetime
from typing import List
from uuid import UUID
from beanie.operators import RegEx
from beanie.odm.operators.find.logical import Or
from fastapi import APIRouter, Depends, HTTPException
import pykakasi
from jamdict import Jamdict
from auth.oauth2 import get_current_user
import re

from schemas.dictionary import (
    DictionaryBase, DictionaryMassSearch, DictionaryCreate)
from models.user import User
from models.dictionary import Dictionary
from dicts import hiragana_full

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
            "kanji": entry.kanji_forms[0].text if len(entry.kanji_forms) > 0 else None,
            "hiragana": hiragana,
            "katakana": entry.kana_forms[-1].text if (len(entry.kana_forms) > 1 and bool(re.match(r'^[\u30A0-\u30FF]+$', entry.kana_forms[-1].text))) else None,
            "romaji": kks.convert(hiragana)[0]['hepburn'],
            "transliteration": hiragana_to_ukrainian(hiragana),
            "kunyomi": kanji_info.chars[0].rm_groups[0].kun_readings[0].value if len(kanji_info.chars) > 0 else None,
            "onyomi": kanji_info.chars[0].rm_groups[0].on_readings[0].value if len(kanji_info.chars) > 0 else None,
            "en_translation": entry.senses[0].gloss[0].text,
            "ua_translation": None,
        })

    return results


def hiragana_to_ukrainian(hira):
    htudict = hiragana_full
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
async def create_entry(request: DictionaryCreate, current_user: User = Depends(get_current_user)):

    print(request.model_dump_json())

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
        created_by=current_user.id,
        approved=current_user.role.name == "linguist",
        approved_by=current_user if current_user.role.name == "linguist" else None
    )

    print(dictionary.model_dump_json())

    try:
        await dictionary.save()
        return dictionary
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Error: {e}"
        )


@router.get("/entry/{uuid}", response_model=DictionaryBase)
async def get_entry_by_uuid(uuid: UUID):
    try:
        dic = await Dictionary.find_one(Dictionary.uuid == uuid)
        return dic
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Error: {e}"
        )


@router.post("/entry/{uuid}")
async def update_entry_by_uuid(request: DictionaryCreate, uuid: UUID, current_user: User = Depends(get_current_user)):
    try:
        dic = await Dictionary.find_one(Dictionary.uuid == uuid)
        dic.kanji = request.kanji
        dic.hiragana = request.hiragana
        dic.katakana = request.katakana
        dic.romaji = request.romaji
        dic.transliteration = request.transliteration
        dic.kunyomi = request.kunyomi
        dic.onyomi = request.onyomi
        dic.en_translation = request.en_translation
        dic.ua_translation = request.ua_translation
        dic.updated_at = datetime.now()
        await dic.save()
        return dic
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Error: {e}"
        )


@router.patch("/entry/{uuid}", response_model=DictionaryBase)
async def approve_entry(uuid: UUID, current_user: User = Depends(get_current_user)):
    try:
        dic = await Dictionary.find_one(Dictionary.uuid == uuid)
        dic.approved_by = current_user
        dic.approved = True
        await dic.save()
        return dic
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Error: {e}"
        )


@router.delete("/entry/{uuid}", response_model=DictionaryBase)
async def delete_entry_by_uuid(uuid: UUID):
    try:
        dic = await Dictionary.find_one(Dictionary.uuid == uuid)
        await dic.delete()
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
        dic = await Dictionary.find_all(fetch_links=True, nesting_depths_per_field={"collections": 0,
                                                                                    "approved_by": 1}).to_list()
        return dic
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Error: {e}"
        )


@router.get("/search/{query}", response_model=DictionaryMassSearch)
async def search(query: str):
    dic = await Dictionary.find_many(Or(
        RegEx(Dictionary.kanji, query, 'i'),
        RegEx(Dictionary.hiragana, query, 'i'),
        RegEx(Dictionary.katakana, query, 'i'),
        RegEx(Dictionary.ua_translation, query, 'i'),
        RegEx(Dictionary.romaji, query, 'i')
    )).to_list()

    dic_base_list = [DictionaryBase(**d.model_dump())
                     for d in dic if d.approved]
    local = get_kanji_info(query)

    filtered_local = [l for l in local if l['idseq']
                      not in [d.idseq for d in dic_base_list]]

    results = DictionaryMassSearch(
        en_sourse=filtered_local, ua_sourse=dic_base_list)

    return results


@ router.get("/jamdict/{idseq}")
def get_jamdict(idseq: int):
    result = get_kanji_info(idseq)[0]

    return result
