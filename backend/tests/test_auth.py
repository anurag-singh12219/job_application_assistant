import pytest
from datetime import datetime, timedelta, timezone
from db.models import EmailVerificationToken, PasswordResetToken, RefreshToken, User
from core.security import hash_token, get_password_hash, generate_secure_token


def test_successful_registration(client, db_session):
    payload = {
        "full_name": "John Doe",
        "email": "john.doe@example.com",
        "password": "SecurePassword123!",
        "confirm_password": "SecurePassword123!",
        "accept_terms": True
    }
    response = client.post("/api/auth/register", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "Registration successful" in data["message"]
    assert data["user"]["email"] == "john.doe@example.com"
    assert data["user"]["role"] == "user"  # Least privilege

    # Verify user exists in database with Argon2 hash and verification token
    db_session.expire_all()
    db_user = db_session.query(User).filter(User.email == "john.doe@example.com").first()
    assert db_user is not None
    assert db_user.password_hash.startswith("$argon2id$")
    assert db_user.is_email_verified is False

    verify_token = db_session.query(EmailVerificationToken).filter_by(user_id=db_user.id).first()
    assert verify_token is not None


def test_duplicate_email_handling(client, test_user):
    payload = {
        "full_name": "Another User",
        "email": "alice@example.com",  # Same as test_user
        "password": "AnotherPassword123!",
        "confirm_password": "AnotherPassword123!",
        "accept_terms": True
    }
    response = client.post("/api/auth/register", json=payload)
    assert response.status_code == 400
    assert "Unable to complete registration" in response.json()["detail"]


def test_weak_password_rejection(client):
    # Too short
    res1 = client.post("/api/auth/register", json={
        "full_name": "Short Pwd",
        "email": "short@example.com",
        "password": "Short1!",
        "confirm_password": "Short1!"
    })
    assert res1.status_code == 422

    # Missing special character
    res2 = client.post("/api/auth/register", json={
        "full_name": "No Special",
        "email": "nospecial@example.com",
        "password": "Password123",
        "confirm_password": "Password123"
    })
    assert res2.status_code == 422

    # Passwords do not match
    res3 = client.post("/api/auth/register", json={
        "full_name": "Mismatch",
        "email": "mismatch@example.com",
        "password": "Password123!",
        "confirm_password": "Different123!"
    })
    assert res3.status_code == 422


def test_successful_login(client, test_user):
    response = client.post("/api/auth/login", json={
        "email": "alice@example.com",
        "password": "StrongPass123!",
        "remember_me": True
    })
    assert response.status_code == 200
    assert "Login successful" in response.json()["message"]
    assert "access_token" in response.cookies
    assert "refresh_token" in response.cookies
    assert "csrf_token" in response.cookies


def test_invalid_login(client, test_user):
    response = client.post("/api/auth/login", json={
        "email": "alice@example.com",
        "password": "WrongPassword999!"
    })
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password."


def test_account_lockout_after_failed_attempts(client, test_user, db_session):
    # Perform 5 failed login attempts
    for _ in range(5):
        res = client.post("/api/auth/login", json={
            "email": "alice@example.com",
            "password": "WrongPassword!"
        })
        assert res.status_code == 401

    # 6th attempt should be blocked by account lockout (403)
    locked_res = client.post("/api/auth/login", json={
        "email": "alice@example.com",
        "password": "StrongPass123!"  # Even with correct password!
    })
    assert locked_res.status_code == 403
    assert "temporarily locked" in locked_res.json()["detail"]


def test_logout(client, test_user):
    login_res = client.post("/api/auth/login", json={
        "email": "alice@example.com",
        "password": "StrongPass123!"
    })
    assert login_res.status_code == 200

    logout_res = client.post("/api/auth/logout")
    assert logout_res.status_code == 200
    assert "Logged out successfully" in logout_res.json()["message"]


def test_current_user_endpoint(client, test_user):
    # Unauthenticated request -> 401
    unauth_res = client.get("/api/auth/me")
    assert unauth_res.status_code == 401

    # Authenticate
    login_res = client.post("/api/auth/login", json={
        "email": "alice@example.com",
        "password": "StrongPass123!"
    })
    assert login_res.status_code == 200
    access_token = login_res.cookies.get("access_token")

    # Authenticated request -> 200 via header or cookie
    auth_res = client.get("/api/auth/me", headers={"Authorization": f"Bearer {access_token}"})
    assert auth_res.status_code == 200
    assert auth_res.json()["email"] == "alice@example.com"
    assert auth_res.json()["role"] == "user"


def test_refresh_token_rotation_and_reuse_detection(client, test_user, db_session):
    # Log in to get initial refresh token
    login_res = client.post("/api/auth/login", json={
        "email": "alice@example.com",
        "password": "StrongPass123!"
    })
    assert login_res.status_code == 200
    initial_refresh = login_res.cookies.get("refresh_token")
    assert initial_refresh is not None

    # First rotation -> Successful
    client.cookies.set("refresh_token", initial_refresh)
    refresh_res = client.post("/api/auth/refresh")
    assert refresh_res.status_code == 200
    new_refresh = refresh_res.cookies.get("refresh_token")
    assert new_refresh is not None
    assert new_refresh != initial_refresh

    # Reuse old rotated token -> Triggers reuse anomaly detection!
    client.cookies.set("refresh_token", initial_refresh)
    reuse_res = client.post("/api/auth/refresh")
    assert reuse_res.status_code == 401
    assert "anomaly" in reuse_res.json()["detail"].lower()

    # The entire family should now be revoked; even new_refresh should fail!
    client.cookies.set("refresh_token", new_refresh)
    blocked_res = client.post("/api/auth/refresh")
    assert blocked_res.status_code == 401


def test_email_verification(client, db_session):
    # Register user
    reg_res = client.post("/api/auth/register", json={
        "full_name": "Verify Me",
        "email": "verify@example.com",
        "password": "Password123!",
        "confirm_password": "Password123!"
    })
    assert reg_res.status_code == 200

    db_session.expire_all()
    user = db_session.query(User).filter_by(email="verify@example.com").first()
    assert user is not None
    assert user.is_email_verified is False

    # Grab the created token and set a known raw token
    token_entry = db_session.query(EmailVerificationToken).filter_by(user_id=user.id).first()
    assert token_entry is not None
    raw_token = generate_secure_token()
    token_entry.token_hash = hash_token(raw_token)
    db_session.commit()

    # Call verify endpoint
    verify_res = client.post("/api/auth/verify-email", json={"token": raw_token})
    assert verify_res.status_code == 200
    assert "verified successfully" in verify_res.json()["message"]

    db_session.expire_all()
    db_session.refresh(user)
    assert user.is_email_verified is True

    # Reusing the token should fail
    reused_res = client.post("/api/auth/verify-email", json={"token": raw_token})
    assert reused_res.status_code == 400


def test_password_reset_flow(client, test_user, db_session):
    # 1. Request forgot password
    forgot_res = client.post("/api/auth/forgot-password", json={"email": "alice@example.com"})
    assert forgot_res.status_code == 200
    assert "instructions have been sent" in forgot_res.json()["message"]

    # 2. Get reset token
    db_session.expire_all()
    reset_entry = db_session.query(PasswordResetToken).filter_by(user_id=test_user.id).first()
    assert reset_entry is not None
    raw_token = generate_secure_token()
    reset_entry.token_hash = hash_token(raw_token)
    db_session.commit()

    # 3. Reset password
    reset_res = client.post("/api/auth/reset-password", json={
        "token": raw_token,
        "password": "NewBrandPassword123!",
        "confirm_password": "NewBrandPassword123!"
    })
    assert reset_res.status_code == 200

    # 4. Try logging in with old password -> Fails
    old_login = client.post("/api/auth/login", json={
        "email": "alice@example.com",
        "password": "StrongPass123!"
    })
    assert old_login.status_code == 401

    # 5. Try logging in with new password -> Succeeds
    new_login = client.post("/api/auth/login", json={
        "email": "alice@example.com",
        "password": "NewBrandPassword123!"
    })
    assert new_login.status_code == 200


def test_password_change_flow(client, test_user):
    # Login
    login_res = client.post("/api/auth/login", json={
        "email": "alice@example.com",
        "password": "StrongPass123!"
    })
    assert login_res.status_code == 200
    csrf_token = login_res.json().get("csrf_token") or login_res.cookies.get("csrf_token")
    access_token = login_res.cookies.get("access_token")

    # Change password
    headers = {"Authorization": f"Bearer {access_token}"}
    if csrf_token:
        headers["X-CSRF-Token"] = csrf_token

    change_res = client.patch(
        "/api/auth/change-password",
        headers=headers,
        json={
            "current_password": "StrongPass123!",
            "new_password": "UpdatedPassword456!",
            "confirm_new_password": "UpdatedPassword456!"
        }
    )
    assert change_res.status_code == 200

    # Login with new password
    new_login = client.post("/api/auth/login", json={
        "email": "alice@example.com",
        "password": "UpdatedPassword456!"
    })
    assert new_login.status_code == 200


def test_inactive_user_cannot_login(client, test_user, db_session):
    test_user.is_active = False
    db_session.commit()

    login_res = client.post("/api/auth/login", json={
        "email": "alice@example.com",
        "password": "StrongPass123!"
    })
    assert login_res.status_code == 403
    assert "deactivated" in login_res.json()["detail"].lower()
