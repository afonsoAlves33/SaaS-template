from project.db.exceptions import ExistingDataError
from project.db.schemas import UserSchema
from project.db.models import UserModel
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from project.auth.utils import __get_password_hash as get_passwd_hash
from project.decorators import log_errors

class UserUseCases:
    @log_errors
    def __init__(self, db_session: Session):
        self.db_session = db_session
        pass

    @log_errors
    def create_user(self, user: UserSchema):
        user_model = UserModel(
            username=user.username,
            password=get_passwd_hash(user.password)
        )
        try:
            self.db_session.add(user_model)
            self.db_session.commit()
        except IntegrityError:
            # This error occurs when the user try to create a person who already exists
            raise ExistingDataError(description="User already exists")

    @log_errors
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
