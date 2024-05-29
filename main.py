from auth import authentication
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from routers import (user,
                     role,
                     dictionary,
                     collection,
                     quiz)

from models.role import Role
from models.user import User
from models.dictionary import Dictionary
from models.collection import Collection
from models.stats import Stats

from database.hash import Hash

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Setup mongoDB
    app.client = AsyncIOMotorClient(
        settings.MONGO_HOST,
        settings.MONGO_PORT,
        username=settings.MONGO_USER,
        password=settings.MONGO_PASSWORD,
    )
    await init_beanie(database=app.client[settings.MONGO_DB], document_models=[User, Role, Dictionary, Collection, Stats])

    role_admin = await Role.find_one({"name": "admin"})
    role_linguist = await Role.find_one({"name": "linguist"})
    role_user = await Role.find_one({"name": "user"})

    if not role_admin:
        role_admin = Role(name="admin")
        await role_admin.create()
    if not role_linguist:
        role_linguist = Role(name="linguist")
        await role_linguist.create()
    if not role_user:
        role_user = Role(name="user")
        await role_user.create()

    user = await User.find_one({"email": settings.ADMIN_EMAIL})
    if not user:
        user = User(
            email=settings.ADMIN_EMAIL,
            password=Hash.bcrypt(settings.ADMIN_PASSWORD),
            username="admin",
            role=role_admin,
            stats=await Stats().create(),
            avatar_url=f"{settings.APP_URL}/static/images/blank_avatar.jpg"
        )
        await user.create()

    yield


# from database import models
# from database.database import engine
# from routers import role, user, dictionary


app = FastAPI(lifespan=lifespan)
app.include_router(authentication.router)
app.include_router(role.router)
app.include_router(user.router)
app.include_router(dictionary.router)
app.include_router(collection.router)
app.include_router(quiz.router)


@app.get("/hello")
def index():
    return {"message": "Hello, World!"}


# models.Base.metadata.create_all(engine)


origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")
