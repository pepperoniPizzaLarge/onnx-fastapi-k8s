from datetime import datetime, timezone, timedelta
from argon2 import PasswordHasher
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from starlette import status
from sqlalchemy.orm import Session

from database.db import SessionLocal
from database.sql_models import Users
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError

router = APIRouter(
    prefix="/auth",
    tags=['auth']
)

JWT_SECRET = "8a1fc1e8922b38d6ce50d4acd5c795cfd1dc5c8680197d5439a50e2bc686"  # generated using git bash openssl
JWT_HASH_AlG = "HS256"

# the client (the frontend running in the user's browser)
# must send username and pw to a specific URL in the  API (declared here with tokenUrl="auth/token") to get the JWT
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")


class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str


class Token(BaseModel):
    access_token: str
    token_type: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]


def hash_password(password: str):
    """Hash user password"""
    ph = PasswordHasher()
    bytes = password.encode('utf-8')
    hex_encoded_hash = ph.hash(bytes)
    
    return hex_encoded_hash


def authenticate_user(username: str, password: str, db):
    """Authenticate user in the database"""
    user = db.query(Users).filter(Users.username==username).first()
    ph = PasswordHasher()
    
    if not user:
        return False
    elif not ph.verify(user.hashed_password, password):
        return False
    else:
        return user


def create_access_token(username: str, user_id: int, expires_delta=timedelta):
    """Create the JWT Token"""
    encode = {"sub": username, "id": user_id}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({"exp": expires})

    return jwt.encode(encode, JWT_SECRET, algorithm=JWT_HASH_AlG)
    

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_HASH_AlG])
        username: str = payload.get('sub')  # set "sub" as username above
        user_id: int = payload.get('id')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Could not validate user.")
            
        return {"username": username, "user_id": user_id}

    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Could not validate user.")
        

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, 
                      create_user_request: CreateUserRequest):
    
    create_user_model = Users(
        email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        role=create_user_request.role,
        hashed_password=hash_password(create_user_request.password),
        is_active=True 
    )
    
    db.add(create_user_model)
    db.commit()


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db: db_dependency):
    """Return the JWT to the user/client"""
    user = authenticate_user(form_data.username, form_data.password, db)
    
    if user is False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Could not validate user.")
    
    token = create_access_token(user.username, user.id, timedelta(minutes=20))
    
    return {"access_token": token, "token_type": "bearer"}
