from src.bootstrap import user_id_generator, account_number_generator
from src.configs.database import SessionLocal


def get_session_factory():
    return SessionLocal


def get_user_id_generator():
    return user_id_generator


def get_account_number_generator():
    return account_number_generator
