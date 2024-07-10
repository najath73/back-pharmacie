from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta
from models.user import User, Role
from utils.auth import ACCESS_TOKEN_EXPIRE_MINUTES, verify_password, create_access_token
from models.token import Token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

router = APIRouter(tags=["Auth"])



@router.post("/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await User.find_one(User.username == form_data.username)
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"email": user.email, "roles": user.roles}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}