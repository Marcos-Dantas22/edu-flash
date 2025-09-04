import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.config import settings
from core.database import Base  

@pytest.fixture(scope="function")  # mudar para function garante sessão limpa por teste
def test_db():
    # Cria engine pro banco de teste
    engine = create_engine(settings.TEST_DATABASE_URL)
    TestingSessionLocal = sessionmaker(bind=engine)

    # Cria todas as tabelas
    Base.metadata.create_all(engine)

    # Cria a sessão
    session = TestingSessionLocal()
    try:
        yield session  # fornece a sessão para o teste
    finally:
        session.rollback()  # desfaz alterações
        session.close()     # fecha a conexão
        Base.metadata.drop_all(engine)  # limpa tabelas