import pytest
import os
from dotenv import load_dotenv
from alembic.config import Config
from alembic import command
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from models.model import Base

load_dotenv()

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_DB = os.getenv("POSTGRES_DB")

TEST_DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def test_db_session():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="session")
def alembic_config():
    config = Config("alembic.ini")  # Укажите путь к вашему файлу конфигурации Alembic
    return config

@pytest.fixture(scope="session")
def run_alembic_upgrade(alembic_config):
    def _run_alembic_upgrade():
        command.upgrade(alembic_config, "head")
    return _run_alembic_upgrade

def test_alembic_migrations(run_alembic_upgrade, test_db_session):
    run_alembic_upgrade()

    sql_query = text("SELECT table_name FROM information_schema.tables WHERE table_name = 'Employee'")
    result = test_db_session.execute(sql_query)
    assert result.scalar() is not None
