import shutil
import uuid
from config import settings
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from auth.oauth2 import get_current_user
from pymongo import errors
from models.collection import Collection
from models.role import Role
from models.dictionary import Dictionary
from schemas.user import (UserBase as UserBaseSchema,
                          UserUpdate as UserUpdateSchema,
                          UserPrivate as UserPrivateSchema,
                          UserPublic as UserPublicSchema,
                          UserStats as UserStatsSchema)
from models.user import User as UserModel
from models.stats import Stats
from helpers.hash import Hash
from beanie.exceptions import RevisionIdWasChanged
from beanie.odm.operators.find.logical import Or

router = APIRouter(
    prefix="/user",
    tags=["User"]
)


@router.post("/", response_model=UserBaseSchema, status_code=status.HTTP_201_CREATED)
async def create(request: UserBaseSchema):

    user = UserModel(
        username=request.username,
        password=Hash.bcrypt(request.password),
        email=request.email,
        role=await Role.find_one(Role.name == "user"),
        stats=await Stats().create())

    try:
        await user.create()
        return user
    except errors.DuplicateKeyError:
        raise HTTPException(
            status_code=400, detail="User with that email or username already exists."
        )


@router.get("/me", response_model=UserPrivateSchema)
async def read_me(current_user: UserPrivateSchema = Depends(get_current_user)):
    return current_user


@router.get("/me/stats", response_model=UserStatsSchema)
async def read_me_stats(current_user: UserPrivateSchema = Depends(get_current_user)):
    return current_user


@router.patch("/me", response_model=UserBaseSchema)
async def update(update: UserUpdateSchema, current_user: UserModel = Depends(get_current_user)):
    update_data = update.model_dump(exclude_unset=True)

    if "password" in update_data:
        update_data["password"] = Hash.bcrypt(update_data["password"])

    current_user = current_user.model_copy(update=update_data)

    try:
        await current_user.save()
        return current_user
    except (errors.DuplicateKeyError, RevisionIdWasChanged):
        raise HTTPException(
            status_code=400, detail="User with that email already exists."
        )


@router.delete("/me", response_model=UserPrivateSchema)
async def delete(current_user: UserModel = Depends(get_current_user)):
    user = await UserModel.find_one(UserModel.id == current_user.id)

    if user.collections:
        for collection_link in user.collections:
            collection = await Collection.get(collection_link.id)
            if collection:
                await collection.delete()

    dictionaries_created_by_user = await Dictionary.find(Dictionary.created_by.id == user.id).to_list()
    for dictionary in dictionaries_created_by_user:
        await dictionary.delete()

    dictionaries_approved_by_user = await Dictionary.find(Dictionary.approved_by.id == user.id).to_list()
    for dictionary in dictionaries_approved_by_user:
        dictionary.approved_by = None
        await dictionary.save()

    await user.delete()

    return current_user


@router.get("/{username}", response_model=UserPublicSchema)
async def get_user(username: str):
    user = await UserModel.find_one(UserModel.username == username, fetch_links=True)

    user.collections = [c for c in user.collections if c.is_public]

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/upload_avatar", response_model=UserPrivateSchema)
async def upload_avatar(image: UploadFile = File(...), current_user: UserModel = Depends(get_current_user)):
    new_avatar = f'{uuid.uuid4()}.'
    filename = new_avatar.join(image.filename.rsplit('.', 1))
    path = f'static/images/{filename}'

    with open(path, 'w+b') as buffer:
        shutil.copyfileobj(image.file, buffer)

    avatar_url = f'{settings.APP_URL}/{path}'

    current_user.avatar_url = avatar_url

    await current_user.save()

    return current_user
