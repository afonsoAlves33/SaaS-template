from datetime import datetime, timedelta, timezone
from typing import Annotated
from project.db.schemas import UserSchema
from project.auth.use_cases import UserUseCases
from fastapi import Depends, FastAPI, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from pydantic import BaseModel
from project.db.database import get_db
from sqlalchemy.orm import Session
from project.models.user import UserModel
import jwt

SECRET_KEY = "680c4caa9dd1ffcdb60c27cf432ab3fdda5caa4b5c6b9c6fc159800cee75c01f"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

router_auth = APIRouter(prefix='/auth')

fake_users_db = {
    # template
    "UserName": {
        "username": "UserName",
        "password": "Example.ou40KRVeVGxwXatjW/OwsHGxyWEgXNNLhbKpYVHvIHyMZ0zMoO"
    }
}
"""
TODO:

TESTS


"""


def add_person_to_dict(
        user: UserSchema | UserModel
):
    """
    Testar com UserSchema!!
    :param user: a user you want to add to the fake_db dict, type: UserModel | UserSchema
    :return:
    """
    try:
        user_dict = user.__dict__
        fake_users_db[str(user_dict['username'])] = {
            "username": str(user_dict['username']),
            "password": str(user_dict['password'])
        }
    except Exception as e:
        print(e)
        raise Exception(f"Problem while trying to add user {user.username} to the 'fake_db' dict!")
    return True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        user_dict['hashed_password'] = user_dict['password']
        return UserInDB(**user_dict)


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@router_auth.post("/token")
async def login_for_access_token(
    user: UserSchema,
    db_session: Session = Depends(get_db)
) -> Token:
    uc = UserUseCases(db_session=db_session)
    user_from_db = uc.find_user_from_username(user)
    if user_from_db:
        add_person_to_dict(user_from_db)
    user = authenticate_user(fake_users_db, str(user.username), str(user.password))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@router_auth.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user


@router_auth.get("/users/me/items/")
async def read_own_items(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return [{"item_id": "Foo", "owner": current_user.username}]