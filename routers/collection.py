import os
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from slugify import slugify
from auth.oauth2 import get_current_user
import genanki
from models.user import User
from models.dictionary import Dictionary
from models.collection import Collection
from schemas.collection import CollectionBase, CollectionCreate, CollectionUpdate

ANKI_MODEL_ID = 1424945485
ANKI_DECK_ID = 1517805082

router = APIRouter(
    prefix="/collection",
    tags=["Collection"]
)


def generate_anki_deck(collection):
    model = genanki.Model(
        ANKI_MODEL_ID,
        'Japanese',
        fields=[
            {'name': 'Kanji'},
            {'name': 'Hiragana'},
            {'name': 'Katakana'},
            {'name': 'Transliteration'},
            {'name': 'Ua_Translation'}
        ],
        templates=[
            {
                'name': 'Card 1',
                'qfmt': '{{Kanji}}',
                'afmt': '{{FrontSide}}<br>{{Hiragana}} ({{Katakana}})<br>{{Transliteration}}<br>{{Ua_Translation}}',
            }
        ]
    )

    deck = genanki.Deck(ANKI_DECK_ID, collection.get('name'))

    for word in collection.get('words'):
        note = genanki.Note(
            model=model,
            fields=[
                word.get('kanji'),
                word.get('hiragana'),
                word.get('katakana') if word.get('katakana') else '',
                word.get('transliteration'),
                word.get('ua_translation')
            ]
        )
        deck.add_note(note)

    package = genanki.Package(deck)

    if not os.path.exists('static/files'):
        os.makedirs('static/files')

    out = f'static/files/{slugify(collection.get("name"))}.apkg'

    package.write_to_file(out)

    return out


@ router.post("/", response_model=CollectionBase, status_code=status.HTTP_201_CREATED)
async def create(request: CollectionCreate, current_user: User = Depends(get_current_user)):
    print(request.model_dump_json())
    collection = Collection(
        name=request.name,
        description=request.description,
        is_public=request.is_public
    )

    await collection.create()

    user = await User.find_one(User.id == current_user.id)

    user.collections.append(collection)

    await user.save()

    return collection


@ router.get("/{uuid}", response_model=CollectionBase)
async def get_collection_by_uuid(uuid: UUID):
    collection = await Collection.find(Collection.uuid == uuid, fetch_links=True).first_or_none()

    # if not collection.is_public:
    #     raise HTTPException(
    #         status_code=400, detail="Collection is private."
    #     )

    return collection


@ router.patch("/{uuid}", response_model=CollectionUpdate)
async def update_collection_by_uuid(request: CollectionUpdate, uuid: UUID, current_user: User = Depends(get_current_user)):
    collection = await Collection.find_one(Collection.uuid == uuid, fetch_links=True, nesting_depth=1)

    if collection.id not in [c.id for c in current_user.collections]:
        raise HTTPException(
            status_code=400, detail="You don't have permission to edit this collection."
        )

    collection.name = request.name if request.name else collection.name
    collection.description = request.description if request.description else collection.description
    collection.is_public = request.is_public if request.is_public != collection.is_public else collection.is_public

    await collection.save()

    return collection


@ router.delete("/{uuid}", response_model=CollectionBase)
async def delete_collection_by_uuid(uuid: UUID, current_user: User = Depends(get_current_user)):
    collection = await Collection.find_one(Collection.uuid == uuid, fetch_links=True, nesting_depth=1)

    if collection.id not in [c.id for c in current_user.collections]:
        raise HTTPException(
            status_code=400, detail="You don't have permission to delete this collection."
        )

    await collection.delete()

    raise HTTPException(
        status_code=200, detail="Collection deleted."
    )


@ router.post("/add/{uuid}", response_model=CollectionBase)
async def add_entry_to_collection(uuid: UUID, word_uuid: UUID, current_user: User = Depends(get_current_user)):
    collection = await Collection.find_one(Collection.uuid == uuid, fetch_links=True, nesting_depth=1)

    if collection.id not in [c.id for c in current_user.collections]:
        raise HTTPException(
            status_code=400, detail="You don't have permission to edit this collection."
        )

    dic = await Dictionary.find_one(Dictionary.uuid == word_uuid)

    if dic.id in [d.id for d in collection.words]:
        raise HTTPException(
            status_code=400, detail="This word is already in the collection."
        )

    collection.words.append(dic)

    await collection.save()

    return collection


@ router.delete("/remove/{uuid}", response_model=CollectionBase)
async def remove_entry_from_collection(uuid: UUID, word_uuid: UUID, current_user: User = Depends(get_current_user)):
    collection = await Collection.find_one(Collection.uuid == uuid, fetch_links=True, nesting_depth=1)

    if collection.id not in [c.id for c in current_user.collections]:
        raise HTTPException(
            status_code=400, detail="You don't have permission to edit this collection."
        )

    dic = await Dictionary.find_one(Dictionary.uuid == word_uuid)

    if dic.id not in [d.id for d in collection.words]:
        raise HTTPException(
            status_code=400, detail="This word is not in the collection."
        )

    collection.words = [d for d in collection.words if d.id != dic.id]

    await collection.save()

    return collection


@router.get("/download/{uuid}")
async def download_collection(uuid: UUID):
    collection = await Collection.find_one(Collection.uuid == uuid, fetch_links=True, nesting_depth=1)

    filepath = generate_anki_deck(collection.model_dump(mode='python'))

    return FileResponse(filepath, filename=filepath.split('/')[-1])
