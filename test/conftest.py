import pytest

from models.user import User


@pytest.fixture(autouse=True)
def create_dummy_user(tmpdir):
    """Fixture to execute asserts before and after a test is run"""
    from conf_test_db import override_get_db
    database = next(override_get_db())
    new_user = User(username='user@gmail.com', email='user@gmail.com', password='1234')
    database.add(new_user)
    database.commit()

    yield

    database.query(User).filter(User.email == 'user@gmail.com').delete()
    database.commit()
