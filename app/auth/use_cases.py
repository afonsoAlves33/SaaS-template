from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from starlette import status
from auth.schemas import UserSchema
from passlib.context import CryptContext
from db.models import UserModel

crypt_context = CryptContext(schemes=['sha256_crypt'])


class UserUserCases:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create_user(self, user: UserSchema):
        user_model = UserModel(
            username=user.username,
            password=crypt_context.hash(user.password)
        )
        try:
            self.db_session.add(user_model)
            self.db_session.commit()
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='User already exists'
            )
