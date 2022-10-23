import pytest

from yo1k.api_yatube import schemas


@pytest.fixture()
def user_in():
    return schemas.UserCreate(
            username="Tester",
            password="test_password"
    )

@pytest.fixture()
def user_in_2():
    return schemas.UserCreate(
            username="Tester2",
            password="test_password"
    )
