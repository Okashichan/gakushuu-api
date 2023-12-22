from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from database import models
from database.database import engine
from auth import authentication
from routers import role, user, dictionary


app = FastAPI()
app.include_router(authentication.router)
app.include_router(role.router)
app.include_router(user.router)
app.include_router(dictionary.router)


@app.get("/hello")
def index():
    return {"message": "Hello, World!"}


models.Base.metadata.create_all(engine)


origins = [
    'http://localhost:3000'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")
