from typing import List

from fastapi import APIRouter, Depends
from starlette import status

from src.accounts.application.services import AccountService
from src.accounts.application.unit_of_work import SqlAccountUnitOfWork
from src.accounts.domain import models
from src.accounts.dto import CreateAccountInfo, AccountPassword, AccountNumber
from src.dependencies import get_session_factory, get_account_number_generator
from src.security.routers import authorize

router = APIRouter(
    prefix="/api/accounts"
)


@router.post("", status_code=status.HTTP_201_CREATED)
def create_account(
        account_password: AccountPassword,
        user_id=Depends(authorize),
        session_factory=Depends(get_session_factory),
        account_number_generator=Depends(get_account_number_generator)
):
    info = CreateAccountInfo(owner_id=user_id, account_password=account_password.value)
    account_service = AccountService(account_number_generator, SqlAccountUnitOfWork(session_factory))
    account_service.create_account_with(info)


@router.get("", status_code=status.HTTP_200_OK, response_model=List[models.Account])
def get_account_list(
        user_id=Depends(authorize),
        session_factory=Depends(get_session_factory),
        account_number_generator=Depends(get_account_number_generator)
):
    account_service = AccountService(account_number_generator, SqlAccountUnitOfWork(session_factory))
    return account_service.list_accounts_with(owner_id=user_id)


@router.get("/{account_number}", status_code=status.HTTP_200_OK)
def get_account(
        account_number: str,
        user_id=Depends(authorize),
        session_factory=Depends(get_session_factory),
        account_number_generator=Depends(get_account_number_generator)
):
    account_service = AccountService(account_number_generator, SqlAccountUnitOfWork(session_factory))
    return account_service.retrieve_account_with(account_number)