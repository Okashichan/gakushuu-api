from datetime import datetime
from typing import List
from uuid import UUID
from beanie.operators import RegEx
from beanie.odm.operators.find.logical import Or
from fastapi import APIRouter, Depends, HTTPException
from auth.oauth2 import get_current_user
from schemas.dictionary import (
    DictionaryBase, DictionaryMassSearch, DictionaryCreate)
from models.user import User
from models.dictionary import Dictionary
from helpers.dicts import get_kanji_info

router = APIRouter(
    prefix="/dictionary",
    tags=["Dictionary"]
)


@router.post("/")
async def create_entry(request: DictionaryCreate, current_user: User = Depends(get_current_user)):
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
    result = get_kanji_info(idseq, deeplapi=True)[0]

    return result
