from fastapi import APIRouter, Depends, Header

from src.dependencies import get_session_factory
from src.security.application.services import AuthenticationService, authenticate_token
from src.security.dto import LoginInfo, AccessToken
from src.users.application.unit_of_work import SqlUserUnitOfWork

router = APIRouter(
    prefix="/api/auth"
)


def authorize(authorization: str = Header(None)):
    return authenticate_token(authorization)


@router.post("/login", response_model=AccessToken)
def login(
        info: LoginInfo,
        session_factory=Depends(get_session_factory)
):
    authentication_service = AuthenticationService(uow=SqlUserUnitOfWork(session_factory))
    return authentication_service.authenticate(info)
