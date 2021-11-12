# from fastapi.testclient import TestClient
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
#
# from src import dependencies
# from src.configs.database import Base
# from src.main import app
#
#
# engine = create_engine(
#     "sqlite:///test.db", connect_args={"check_same_thread": False}
# )
# TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#
#
# def test_session_factory():
#     Base.metadata.create_all(bind=engine)
#     print("setup")
#     yield TestingSessionLocal
#     # Base.metadata.drop_all(bind=engine)
#     print("teardown")
#
#
# app.dependency_overrides[dependencies.get_session_factory] = test_session_factory
# client = TestClient(app)
