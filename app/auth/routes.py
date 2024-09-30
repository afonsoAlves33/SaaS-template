from fastapi import APIRouter, Depends, Response
from requests import Session
from starlette import status
from auth.schemas import UserSchema
from auth.use_cases import UserUserCases
from db.main import get_db_session

router = APIRouter(prefix='/user')

@router.post('/register')
def register_user(
        user: UserSchema,
        db_session: Session = Depends(get_db_session()),
):
    uc = UserUserCases(db_session=db_session)
    uc.create_user(user=user)
    return Response(
        content={'msg': 'success'},
        status_code=status.HTTP_201_CREATED
    )