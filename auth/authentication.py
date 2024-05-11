from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from database.hash import Hash
from auth import oauth2

from models.user import User

router = APIRouter(
    tags=["authentication"]
)


@router.post("/token")
async def get_token(request: OAuth2PasswordRequestForm = Depends()):
    user = await User.find_one({"username": request.username})

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid Credentials")

    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"Incorrect password")

    access_token = oauth2.create_access_token(data={"sub": user.username})

    return {"access_token": access_token, "token_type": "bearer"}
