import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.config import settings
from core.database import Base  

@pytest.fixture(scope="session")
def test_db():
    # Cria engine pro banco de teste
    engine = create_engine(settings.TEST_DATABASE_URL)
    TestingSessionLocal = sessionmaker(bind=engine)

    # Cria todas as tabelas
    #TODO: substituir depois pelo alembic
    Base.metadata.create_all(engine)
    yield TestingSessionLocal()  # fornece a sessão para os testes

    # Limpa tabelas depois dos testes
    Base.metadata.drop_all(engine)
