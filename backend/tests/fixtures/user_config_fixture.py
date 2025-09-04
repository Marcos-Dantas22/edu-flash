import pytest
from modules.users.models import UserConfig
from modules.users.utils import LanguageEnum

@pytest.fixture
def fake_user_config(test_db):
    config = UserConfig(language=LanguageEnum.ENGLISH, dark_mode=True)
    test_db.add(config)
    test_db.commit()
    test_db.refresh(config)
    return config
