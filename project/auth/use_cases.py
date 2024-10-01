from fastapi import HTTPException

from starlette import status
from project.db.schemas import UserSchema
from project.models.user import UserModel
from project.auth import hasher as h
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session


class UserUseCases:
    def __init__(self, db_session: Session):
        self.db_session = db_session
        pass


    def create_user(self, user: UserSchema):
        user_model = UserModel(
            name=user.username,
            password=h.get_password_hash(user.password)
        )
        try:
            self.db_session.add(user_model)
            self.db_session.commit()
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='User already exists'
            )

    def find_user(self, user: UserSchema):
        # query = f"""
        #     SELECT * FROM users
        #     WHERE name = '{user.username}'
        #     LIMIT 1;
        # """
        try:
            result = self.db_session.query(UserModel)
        except Exception:
            raise Exception("Something happend: ",str(e))

        if result:
            print(result)
            return result
        return None