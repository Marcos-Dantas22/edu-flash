from datetime import datetime
from modules.users.models import UserConfig
from modules.users.utils import LanguageEnum
from faker import Faker

fake = Faker()


def test_create_user_config(test_db):
    user_config = UserConfig(
        dark_mode=True,
        language=LanguageEnum.ENGLISH
    )
    test_db.add(user_config)
    test_db.commit()
    test_db.refresh(user_config)

    db_config = test_db.query(UserConfig).filter_by(id=user_config.id).first()
    assert db_config is not None
    assert db_config.dark_mode is True
    assert db_config.language == LanguageEnum.ENGLISH
    assert db_config.created is not None
    assert db_config.last_update is not None


def test_user_config_defaults(test_db):
    user_config = UserConfig()  # não passa nada, deve usar valores padrão
    test_db.add(user_config)
    test_db.commit()
    test_db.refresh(user_config)

    assert user_config.dark_mode is False
    assert user_config.language == LanguageEnum.PORTUGUESE_BR
    assert user_config.created is not None
    assert user_config.last_update is not None
