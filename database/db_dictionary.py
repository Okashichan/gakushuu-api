from fastapi import HTTPException, status
from routers.schemas import DictionaryBase
from sqlalchemy.orm.session import Session
from database.models import DbDictionary


def create(db: Session, request: DictionaryBase):
    new_dictionary = DbDictionary(original=request.original,
                                  en_translation=request.en_translation,
                                  ua_translation=request.ua_translation,
                                  romanization=request.romanization,
                                  transliteration=request.transliteration,
                                  comment=request.comment,
                                  created_at=request.created_at,
                                  last_modified=request.last_modified,
                                  author_id=request.author_id,
                                  )

    db.add(new_dictionary)
    db.commit()
    db.refresh(new_dictionary)

    return new_dictionary


def update(db: Session, request: DictionaryBase, dictionary_id: int):
    dictionary = db.query(DbDictionary).filter(
        DbDictionary.id == dictionary_id).first()

    if not dictionary:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Dictionary with id {dictionary_id} not found")

    dictionary.original = request.original
    dictionary.en_translation = request.en_translation
    dictionary.ua_translation = request.ua_translation
    dictionary.romanization = request.romanization
    dictionary.transliteration = request.transliteration
    dictionary.comment = request.comment
    dictionary.last_modified = request.last_modified

    db.commit()
    db.refresh(dictionary)

    return {"message": f"Dictionary with id {dictionary_id} updated"}


def delete(db: Session, dictionary_id: int):
    dictionary = db.query(DbDictionary).filter(
        DbDictionary.id == dictionary_id).first()

    if not dictionary:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Dictionary with id {dictionary_id} not found")

    db.delete(dictionary)
    db.commit()

    return {"message": f"Dictionary with id {dictionary_id} deleted"}


def get_entry_by_original_name(db: Session, original: str):
    word = db.query(DbDictionary).filter(
        DbDictionary.original == original).all()

    if not word:
        return None
        # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        #                     detail=f"Word with original name {original} not found")

    return word


def get_all_entries(db: Session):
    entries = db.query(DbDictionary).limit(100).all()

    if not entries:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Entries not found")

    return entries
