from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta
from models.pharmacy import Pharmacy
from models.user import PharmacyEmploye, User, UserInfo
from utils.auth import ACCESS_TOKEN_EXPIRE_MINUTES, decode_access_token, verify_password, create_access_token
from models.token import Token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

router = APIRouter(prefix="/auth",tags=["Auth"])



@router.post("/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await User.find_one(User.username == form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"email": user.email, "user_id": str(user.id), "role": user.role}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer", "role": user.role}


@router.get("/me", response_model=UserInfo)
async def get_user_info(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(token)
        user = await User.find_one(User.email == payload.get("email"))
        if user is None:
            raise credentials_exception
        if "pharmacy" in user.role:
            connectedUser = await PharmacyEmploye.find_one(PharmacyEmploye.user.id == ObjectId(user.id), fetch_links=True)

            userInfo = {
                "id": str(user.id),
                "username": user.username,
                "email": user.email,
                "role": user.role,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "pharmacy": {
                    "id": str(connectedUser.pharmacy.id),
                    "name": connectedUser.pharmacy.name
                }
            }
            return userInfo
        return {
            "id": str(user.id),
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "first_name": user.first_name,
            "last_name": user.last_name
        }
    except Exception:
        raise credentials_exception