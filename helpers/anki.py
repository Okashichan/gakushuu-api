import genanki
import os
from slugify import slugify

ANKI_MODEL_ID = 1424945485
ANKI_DECK_ID = 1517805082


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
