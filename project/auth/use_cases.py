from typing import Any

from fastapi import HTTPException

from starlette import status
from project.db.schemas import UserSchema
from project.models.user import UserModel
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from project.auth.utils import __get_password_hash as get_passwd_hash

class UserUseCases:
    def __init__(self, db_session: Session):
        self.db_session = db_session
        pass


    def create_user(self, user: UserSchema):
        user_model = UserModel(
            username=user.username,
            password=get_passwd_hash(user.password)
        )
        try:
            self.db_session.add(user_model)
            self.db_session.commit()
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='User already exists'
            )

    def find_user_from_username(self, user: UserSchema) -> UserModel | None:
        """
        :param user: A user of type UserSchema
        :return: a Type[UserModel] if the user is found, if it's not, a None type.
        """
        try:
            result = self.db_session.query(UserModel).filter(UserModel.username == user.username).first()
        except Exception as e:
            print(e)
            raise Exception("Something happened while fetching data from the database")

        if result:
            return result
        return None
