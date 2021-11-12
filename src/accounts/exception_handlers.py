from starlette import status
from starlette.responses import JSONResponse


def lack_of_balance_exception_handler(request, exc):
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": str(exc)})


def account_not_found_exception_handler(request, exc):
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": str(exc)})


def duplicated_account_exception_handler(request, exc):
    return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={"message": str(exc)})
