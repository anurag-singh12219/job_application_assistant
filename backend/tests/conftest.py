import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

import sys
import os

# Ensure backend directory is in python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.database import Base, get_db
from core.security import get_password_hash
from core.rate_limiter import rate_limiter
from db.models import User
from main import app

# Create in-memory SQLite database for testing
TEST_DATABASE_URL = "sqlite:///:memory:"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(autouse=True)
def reset_rate_limits():
    """Reset rate limiter state before and after each test."""
    rate_limiter.reset()
    yield
    rate_limiter.reset()


@pytest.fixture(scope="function")
def db_session():
    """Create fresh database tables for each test and tear them down after."""
    Base.metadata.create_all(bind=test_engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="function")
def client(db_session):
    """FastAPI TestClient with overridden get_db dependency."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def test_user(db_session):
    """Create a verified test user."""
    user = User(
        full_name="Alice Candidate",
        email="alice@example.com",
        password_hash=get_password_hash("StrongPass123!"),
        role="user",
        is_active=True,
        is_email_verified=True,
        failed_login_attempts=0
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture(scope="function")
def test_admin(db_session):
    """Create an administrator user."""
    admin = User(
        full_name="Bob Admin",
        email="admin@example.com",
        password_hash=get_password_hash("AdminPass123!"),
        role="admin",
        is_active=True,
        is_email_verified=True,
        failed_login_attempts=0
    )
    db_session.add(admin)
    db_session.commit()
    db_session.refresh(admin)
    return admin
