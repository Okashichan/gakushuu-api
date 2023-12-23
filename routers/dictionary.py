from fastapi import APIRouter, Depends, HTTPException, Request, status
from typing import List
import pykakasi
from sqlalchemy.orm.session import Session
from auth.oauth2 import get_current_user

from database.database import get_db
from database import db_dictionary
from routers.schemas import DictionaryBase, DictionaryDisplay, DictionaryUpdate, UserBase

from jamdict import Jamdict


router = APIRouter(
    prefix="/dictionary",
    tags=["Dictionary"]
)


def get_info_by_jamdict(id):
    jam = Jamdict()

    kanji_info = jam.lookup(id)

    return {
        "en_translation": kanji_info.entries[0].senses[0].gloss[0].text,
        "original": kanji_info.entries[0].kanji_forms[0].text,
        "romanization": pykakasi.kakasi().convert(kanji_info.entries[0].kanji_forms[0].text)[0]['hepburn'],
        "transliteration": romaji_to_ukrainian(pykakasi.kakasi().convert(kanji_info.entries[0].kanji_forms[0].text)[0]['hepburn'])
    }


def get_kanji_info(kanji):
    jam = Jamdict()
    kks = pykakasi.kakasi()

    result = []

    kanji_info = jam.lookup(kanji)

    print(kanji_info.entries[0].idseq)

    if not kanji_info:
        return "Kanji not found in the dictionary."

    for entry in kanji_info.entries:
        english_translation = entry.senses[0].gloss[0].text
        romaji = kks.convert(kanji)[0]['hepburn']
        comments = ""
        result.append({
            "en_translation": english_translation,
            "romanization": romaji,
            "transliteration": romaji_to_ukrainian(romaji),
            "comment": comments,
            "original": entry.kanji_forms[0].text,
            "id": entry.idseq
        })

    return result


def romaji_to_ukrainian(romaji_text):
    # Define a dictionary mapping Romaji characters to Ukrainian transliterations
    transliteration_dict = {
        'a': 'а',
        'i': 'і',
        'u': 'у',
        'e': 'е',
        'o': 'о',
        'ka': 'ка',
        'ki': 'кі',
        'ku': 'ку',
        'ke': 'ке',
        'ko': 'ко',
        'sa': 'са',
        'shi': 'ші',
        'su': 'су',
        'se': 'се',
        'so': 'со',
        'ta': 'та',
        'chi': 'чі',
        'tsu': 'цу',
        'te': 'те',
        'to': 'то',
        'na': 'на',
        'ni': 'ні',
        'nu': 'ну',
        'ne': 'не',
        'no': 'но',
        'ha': 'ха',
        'hi': 'хі',
        'fu': 'фу',
        'he': 'хе',
        'ho': 'хо',
        'ma': 'ма',
        'mi': 'мі',
        'mu': 'му',
        'me': 'ме',
        'mo': 'мо',
        'ya': 'я',
        'yu': 'ю',
        'yo': 'йо',
        'ra': 'ра',
        'ri': 'рі',
        'ru': 'ру',
        're': 'ре',
        'ro': 'ро',
        'wa': 'ва',
        'wo': 'во',
        'n': 'н',
        'ga': 'ґа',
        'gi': 'ґі',
        'gu': 'ґу',
        'ge': 'ґе',
        'go': 'ґо',
        'za': 'за',
        'ji': 'дзі',  # Note: "ji" is used for the "dji" sound in Japanese
        'zu': 'дзу',  # Note: "zu" is used for the "dzu" sound in Japanese
        'ze': 'зе',
        'zo': 'зо',
        'da': 'да',
        'di': 'ді',  # Note: "di" is used for the "dji" sound in Japanese
        'du': 'ду',
        'de': 'де',
        'do': 'до',
        'ba': 'ба',
        'bi': 'бі',
        'bu': 'бу',
        'be': 'бе',
        'bo': 'бо',
        'pa': 'па',
        'pi': 'пі',
        'pu': 'пу',
        'pe': 'пе',
        'po': 'по',
        'sha': 'ша',
        'shi': 'ші',
        'shu': 'шу',
        'she': 'ше',
        'sho': 'шо',
        'ja': 'джа',
        'ji': 'джі',
        'ju': 'джу',
        'je': 'дже',
        'jo': 'джо',
        'kya': 'к' + 'я',
        'kyu': 'к' + 'ю',
        'kyo': 'к' + 'йо',
        'sha': 'ш' + 'а',
        'shu': 'ш' + 'у',
        'she': 'ш' + 'е',
        'sho': 'ш' + 'о',
        'cha': 'ч' + 'а',
        'chu': 'ч' + 'у',
        'cho': 'ч' + 'о',
        'nya': 'н' + 'я',
        'nyu': 'н' + 'ю',
        'nyo': 'н' + 'йо',
        'hya': 'х' + 'я',
        'hyu': 'х' + 'ю',
        'hyo': 'х' + 'йо',
        'mya': 'м' + 'я',
        'myu': 'м' + 'ю',
        'myo': 'м' + 'йо',
        'rya': 'р' + 'я',
        'ryu': 'р' + 'ю',
        'ryo': 'р' + 'йо',
        # Add more mappings as needed
    }

    # Split the Romaji text into individual words
    words = romaji_text.split()

    # Transliterate each word using the dictionary
    ukrainian_text = ''
    for word in words:
        transliterated_word = ''
        i = 0
        while i < len(word):
            # Check for three-character combinations first
            if i + 2 < len(word) and word[i:i + 3] in transliteration_dict:
                transliterated_word += transliteration_dict[word[i:i + 3]]
                i += 3
            # Check for two-character combinations
            elif i + 1 < len(word) and word[i:i + 2] in transliteration_dict:
                transliterated_word += transliteration_dict[word[i:i + 2]]
                i += 2
            else:
                # Single character mapping
                transliterated_word += transliteration_dict.get(
                    word[i], word[i])
                i += 1

        # Add space between transliterated words
        ukrainian_text += transliterated_word + ' '

    return ukrainian_text.strip()


@router.post("/")
def create(request: DictionaryBase, db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    return db_dictionary.create(db, request)


@router.put("/{dictionary_id}")
def update(dictionary_id: int, request: DictionaryUpdate, db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    return db_dictionary.update(db, request, dictionary_id)


@router.delete("/{dictionary_id}")
def delete(dictionary_id: int, db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    return db_dictionary.delete(db, dictionary_id)


@router.get("/original/{original}", response_model=DictionaryDisplay)
def get_entry_by_original_name(original: str, db: Session = Depends(get_db)):
    return db_dictionary.get_entry_by_original_name(db, original)


@router.get("/all", response_model=List[DictionaryDisplay])
def get_all_entries(db: Session = Depends(get_db)):
    return db_dictionary.get_all_entries(db)


@router.get("/search/{search}")
def search(search: str, db: Session = Depends(get_db)):

    return {
        "en_source": get_kanji_info(search),
        "ua_source": db_dictionary.get_entry_by_original_name(db, search)
    }


@router.get("/jamdict/{id}")
def get_jamdict(id: str, db: Session = Depends(get_db)):
    return get_info_by_jamdict(f'id#{id}')
