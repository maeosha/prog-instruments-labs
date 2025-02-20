import pytest
import os
from main import User, UserDatabase, NetworkService, UserService

def test_user_initialization():
    user = User(user_id=1, name="John", email="john@example.com")
    assert user.user_id == 1
    assert user.name == "John"
    assert user.email == "john@example.com"

def test_user_repr():
    user = User(user_id=1, name="John", email="john@example.com")
    assert repr(user) == "User(id=1, name=John, email=john@example.com)"

@pytest.fixture
def db(tmp_path):
    db_filename = tmp_path / "test_db.json"
    return UserDatabase(str(db_filename))

def test_delete_user(db):
    user = User(1, "John", "john@example.com")
    db.add_user(user)
    db.delete_user(1)
    assert db.db == {}

@pytest.fixture
def user_service(tmp_path):
    db_filename = tmp_path / "test_db.json"
    user_db = UserDatabase(str(db_filename))
    network_service = NetworkService()
    return UserService(user_db, network_service)

def test_register_user_success(user_service, mocker):
    mocker.patch("random.random", return_value=0.8)
    user_service.register_user(1)
    user = user_service.user_db.get_user(1)
    assert user.user_id == 1
    assert user.name == "User1"
    assert user.email == "user1@gmail.com"

def test_register_user_failure(user_service, mocker):
    mocker.patch("random.random", return_value=0.95)
    with pytest.raises(ValueError):
        user_service.register_user(1)
