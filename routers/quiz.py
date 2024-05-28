import random
from fastapi import APIRouter
from dicts import *

router = APIRouter(
    prefix="/quiz",
    tags=["Quiz"]
)


def generate_quiz(questions_dict, quiz_size=10):
    if quiz_size > len(questions_dict):
        quiz_size = len(questions_dict)

    keys = list(questions_dict.keys())
    random.shuffle(keys)
    quiz_keys = keys[:quiz_size]

    quiz = []
    for key in quiz_keys:
        correct_answer = questions_dict[key]
        all_answers = list(questions_dict.values())
        wrong_answers = random.sample(
            [ans for ans in all_answers if ans != correct_answer], 3)

        options = wrong_answers + [correct_answer]
        random.shuffle(options)

        unique_options = list(set(options))
        while len(unique_options) < 4:
            remaining_wrong_answers = [
                ans for ans in all_answers if ans != correct_answer and ans not in unique_options]
            if remaining_wrong_answers:
                new_answer = random.choice(remaining_wrong_answers)
                unique_options.append(new_answer)
            unique_options = list(set(unique_options))

        random.shuffle(unique_options)
        quiz.append((key, correct_answer, unique_options))

    return quiz


@router.get("/hiragana")
async def get_hiragana_quiz(basic: bool = True, combinations: bool = False, kuten: bool = False, kuten_combinations: bool = False, size: int = 10):
    if basic:
        return generate_quiz(hiragana_basic, size)
    if combinations:
        return generate_quiz(hiragana_combinations, size)
    if kuten:
        return generate_quiz(hiragana_kuten, size)
    if kuten_combinations:
        return generate_quiz(hiragana_kuten_combinations, size)
    print('yo')
    return generate_quiz(hiragana_full, size)


@router.get("/katakana")
async def get_katakana_quiz(basic: bool = True, combinations: bool = False, kuten: bool = False, kuten_combinations: bool = False, size: int = 10):
    if basic:
        return generate_quiz(katakana_basic, size)
    if combinations:
        return generate_quiz(katakana_combinations, size)
    if kuten:
        return generate_quiz(katakana_kuten, size)
    if kuten_combinations:
        return generate_quiz(katakana_kuten_combinations, size)
    return generate_quiz(katakana_full, size)
