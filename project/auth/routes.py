from fastapi import APIRouter, Depends, Response
from starlette import status
from project.db.schemas import UserSchema
from project.auth.use_cases import UserUseCases
from project.db.database import get_db


router = APIRouter(prefix='/user')

@router.post('/register')
def register_user(
        user: UserSchema,
        db_session=Depends(get_db),
):
    uc = UserUseCases(db_session=db_session)
    uc.create_user(user=user)
    return Response(
        content={'msg': 'success'},
        status_code=status.HTTP_201_CREATED
    )




