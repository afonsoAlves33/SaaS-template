from passlib.context import CryptContext
from project.decorators import log_errors


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@log_errors
def __verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

@log_errors
def __get_password_hash(password):
    return pwd_context.hash(password)
