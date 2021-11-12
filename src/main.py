from fastapi import FastAPI

from src.users.exception_handlers import empty_name_exception_handler, user_not_found_exception_handler, \
    duplicated_user_exception_handler
from src.users.exceptions import EmptyNameException, UserNotFoundException, DuplicatedUserException
from src.users.routers import router as user_router
from src.security.routers import router as security_router
from src.configs.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(user_router)
app.include_router(security_router)


app.add_exception_handler(EmptyNameException, empty_name_exception_handler)
app.add_exception_handler(UserNotFoundException, user_not_found_exception_handler)
app.add_exception_handler(DuplicatedUserException, duplicated_user_exception_handler)
