from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta
from models.user import User, Role, UserInfo
from utils.auth import ACCESS_TOKEN_EXPIRE_MINUTES, decode_access_token, verify_password, create_access_token, get_password_hash
from models.token import Token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

router = APIRouter(prefix="/auth",tags=["Auth"])



@router.post("/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await User.find_one(User.username == form_data.username)
    print(user.firstname)
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"email": user.email, "roles": user.roles}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserInfo)
async def get_user_info(token: str = Depends(oauth2_scheme)):
    email = decode_access_token(token)  # Vérifie le token et obtient l'email
    user = await User.find_one(User.email == email)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return UserInfo(
        username=user.username,
        name=user.name,
        firstname=user.firstname,
        email=user.email,
        roles=user.roles,
        pharmacy=user.pharmacy.id if user.pharmacy else None
    )