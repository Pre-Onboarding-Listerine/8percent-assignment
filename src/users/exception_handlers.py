from starlette import status
from starlette.responses import JSONResponse


def empty_name_exception_handler(request, exc):
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": str(exc)})


def user_not_found_exception_handler(request, exc):
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": str(exc)})


def duplicated_user_exception_handler(request, exc):
    return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={"message": str(exc)})
