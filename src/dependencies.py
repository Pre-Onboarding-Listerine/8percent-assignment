from src.bootstrap import user_id_generator
from src.configs.database import SessionLocal


def get_session_factory():
    return SessionLocal


def get_user_id_generator():
    return user_id_generator

