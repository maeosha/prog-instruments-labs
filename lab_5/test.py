# Импорты
import pytest
import json
import os
from unittest.mock import Mock, patch
from main import User, UserDatabase, NetworkService, UserService, Application

@pytest.fixture
def user():
    """Создает объект User для тестирования."""
    return User(user_id=1, name="TestUser", email="test@example.com")

@pytest.fixture
def user_db(tmpdir):
    """Создает временную базу данных для тестирования."""
    db_filename = tmpdir.join("test_db.json")
    return UserDatabase(str(db_filename))

@pytest.fixture
def network_service():
    """Создает объект NetworkService для тестирования."""
    return NetworkService()

@pytest.fixture
def user_service(user_db, network_service):
    """Создает объект UserService для тестирования."""
    return UserService(user_db, network_service)

@pytest.fixture
def application():
    """Создает объект Application для тестирования."""
    return Application()

def test_user_initialization(user):
    """Проверяет корректность инициализации объекта User."""
    assert user.user_id == 1
    assert user.name == "TestUser"
    assert user.email == "test@example.com"

def test_user_repr(user):
    """Проверяет корректность строкового представления объекта User."""
    assert repr(user) == "User(id=1, name=TestUser, email=test@example.com)"

def test_user_database_load_db(user_db):
    """Проверяет загрузку базы данных."""
    assert isinstance(user_db.db, dict)
    assert len(user_db.db) == 0

def test_user_database_add_user(user_db, user):
    """Проверяет добавление пользователя в базу данных."""
    user_db.add_user(user)
    assert user.user_id in user_db.db
    assert user_db.db[user.user_id] == user.__dict__

def test_user_database_get_user(user_db, user):
    """Проверяет получение пользователя из базы данных."""
    user_db.add_user(user)
    retrieved_user = user_db.get_user(user.user_id)
    assert retrieved_user.user_id == user.user_id
    assert retrieved_user.name == user.name
    assert retrieved_user.email == user.email

def test_user_database_delete_user(user_db, user):
    """Проверяет удаление пользователя из базы данных."""
    user_db.add_user(user)
    user_db.delete_user(user.user_id)
    assert user.user_id not in user_db.db

# Юнит-тесты для класса NetworkService

def test_network_service_fetch_user_data(network_service):
    """Проверяет успешное получение данных пользователя."""
    with patch("time.sleep", return_value=None):
        user_data = network_service.fetch_user_data(1)
        assert user_data["user_id"] == 1
        assert user_data["name"] == "User1"
        assert user_data["email"] == "user1@gmail.com"

def test_network_service_fetch_user_data_failure(network_service):
    """Проверяет обработку ошибки при получении данных пользователя."""
    with patch("random.random", return_value=0.95), patch("time.sleep", return_value=None):
        with pytest.raises(ValueError):
            network_service.fetch_user_data(1)

# Юнит-тесты для класса UserService

def test_user_service_register_user(user_service):
    """Проверяет регистрацию пользователя."""
    with patch("time.sleep", return_value=None):
        user_service.register_user(1)
        user = user_service.user_db.get_user(1)
        assert user is not None
        assert user.user_id == 1
        assert user.name == "User1"
        assert user.email == "user1@gmail.com"

def test_user_service_get_user_info(user_service, user):
    """Проверяет получение информации о пользователе."""
    user_service.user_db.add_user(user)
    retrieved_user = user_service.get_user_info(user.user_id)
    assert retrieved_user.user_id == user.user_id
    assert retrieved_user.name == user.name
    assert retrieved_user.email == user.email

def test_user_service_delete_user(user_service, user):
    """Проверяет удаление пользователя."""
    user_service.user_db.add_user(user)
    user_service.delete_user(user.user_id)
    assert user_service.user_db.get_user(user.user_id) is None

def test_application_run(application):
    """Проверяет выполнение основного цикла приложения."""
    with patch("time.sleep", return_value=None), patch("logging.info") as mock_logging:
        application.run()
        assert mock_logging.call_count >= 6  # Проверяем, что логируются основные шаги
