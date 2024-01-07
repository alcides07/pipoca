from backend.main import app
from dependencies.authenticated_user import get_authenticated_user
from dependencies.database import get_db
from tests.database import get_db_test


def remove_dependencies():
    app.dependency_overrides[get_authenticated_user] = lambda: True
    app.dependency_overrides[get_db] = get_db_test


def resume_dependencies():
    app.dependency_overrides = {}
