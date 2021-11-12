from fastapi import APIRouter, Depends
from starlette import status

from src.dependencies import get_user_id_generator, get_session_factory
from src.users.application.services import UserService
from src.users.application.unit_of_work import SqlUserUnitOfWork
from src.users.dto import RegisterUserInfo

router = APIRouter(
    prefix="/api/users"
)


@router.post("", status_code=status.HTTP_201_CREATED)
def signup(
        info: RegisterUserInfo,
        id_gen=Depends(get_user_id_generator),
        session_factory=Depends(get_session_factory)):
    user_service = UserService(id_gen, SqlUserUnitOfWork(session_factory))
    user_service.register(info)
