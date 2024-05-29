import random
from typing import List
from fastapi import APIRouter, Depends
from helpers.dicts import (
    hiragana_basic,
    hiragana_combinations,
    hiragana_kuten,
    hiragana_kuten_combinations,
    hiragana_full,
    katakana_basic,
    katakana_combinations,
    katakana_kuten,
    katakana_kuten_combinations,
    katakana_full,
)
from models.stats import Stats
from auth.oauth2 import get_current_user
from schemas.user import UserStats
from helpers.quizes import generate_quiz

router = APIRouter(
    prefix="/quiz",
    tags=["Quiz"]
)


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


@router.post("/hiragana_stats")
async def update_hiragana_stats(stats: List[dict], type: str, current_user: UserStats = Depends(get_current_user)):
    current_stats = await Stats.find_one(Stats.id == current_user.stats.id)

    if type == 'basic':
        for stat in stats:
            answer = stat['answer']
            correct = stat['correct']

            if answer in current_stats.hiragana_basic:
                current_stats.hiragana_basic[answer]['right' if correct else 'wrong'] += 1

    if type == 'combinations':
        for stat in stats:
            answer = stat['answer']
            correct = stat['correct']

            if answer in current_stats.hiragana_kuten_combinations:
                current_stats.hiragana_kuten_combinations[answer]['right' if correct else 'wrong'] += 1

    if type == 'kuten':
        for stat in stats:
            answer = stat['answer']
            correct = stat['correct']

            if answer in current_stats.hiragana_kuten:
                current_stats.hiragana_kuten[answer]['right' if correct else 'wrong'] += 1

    if type == 'all':
        for stat in stats:
            answer = stat['answer']
            correct = stat['correct']

            if answer in current_stats.hiragana_basic:
                current_stats.hiragana_basic[answer]['right' if correct else 'wrong'] += 1

            if answer in current_stats.hiragana_kuten_combinations:
                current_stats.hiragana_kuten_combinations[answer]['right' if correct else 'wrong'] += 1

            if answer in current_stats.hiragana_kuten:
                current_stats.hiragana_kuten[answer]['right' if correct else 'wrong'] += 1

    await current_stats.save()

    return current_stats


@router.post("/katakana_stats")
async def update_katakana_stats(stats: List[dict], type: str, current_user: UserStats = Depends(get_current_user)):
    current_stats = await Stats.find_one(Stats.id == current_user.stats.id)

    if type == 'basic':
        for stat in stats:
            answer = stat['answer']
            correct = stat['correct']

            if answer in current_stats.katakana_basic:
                current_stats.katakana_basic[answer]['right' if correct else 'wrong'] += 1

    if type == 'combinations':
        for stat in stats:
            answer = stat['answer']
            correct = stat['correct']

            if answer in current_stats.katakana_kuten_combinations:
                current_stats.katakana_kuten_combinations[answer]['right' if correct else 'wrong'] += 1

    if type == 'kuten':
        for stat in stats:
            answer = stat['answer']
            correct = stat['correct']

            if answer in current_stats.katakana_kuten:
                current_stats.katakana_kuten[answer]['right' if correct else 'wrong'] += 1

    if type == 'all':
        for stat in stats:
            answer = stat['answer']
            correct = stat['correct']

            if answer in current_stats.katakana_basic:
                current_stats.katakana_basic[answer]['right' if correct else 'wrong'] += 1

            if answer in current_stats.katakana_kuten_combinations:
                current_stats.katakana_kuten_combinations[answer]['right' if correct else 'wrong'] += 1

            if answer in current_stats.katakana_kuten:
                current_stats.katakana_kuten[answer]['right' if correct else 'wrong'] += 1

    await current_stats.save()

    return current_stats
