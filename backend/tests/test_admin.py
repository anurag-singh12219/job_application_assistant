import pytest
from db.models import User


def test_unauthenticated_rejected_from_admin_route(client):
    res = client.get("/api/admin/me")
    assert res.status_code == 401


def test_regular_user_rejected_from_admin_route(client, test_user):
    # Log in as normal user
    client.post("/api/auth/login", json={
        "email": "alice@example.com",
        "password": "StrongPass123!"
    })

    res = client.get("/api/admin/me")
    assert res.status_code == 403
    assert "Administrator access required" in res.json()["detail"]

    users_res = client.get("/api/admin/users")
    assert users_res.status_code == 403


def test_admin_access_to_admin_routes(client, test_admin):
    # Log in as admin
    client.post("/api/auth/login", json={
        "email": "admin@example.com",
        "password": "AdminPass123!"
    })

    me_res = client.get("/api/admin/me")
    assert me_res.status_code == 200
    assert me_res.json()["email"] == "admin@example.com"
    assert me_res.json()["role"] == "admin"

    users_res = client.get("/api/admin/users")
    assert users_res.status_code == 200
    assert "users" in users_res.json()
    assert users_res.json()["total"] >= 1


def test_admin_update_user_status(client, test_admin, test_user, db_session):
    login_res = client.post("/api/auth/login", json={
        "email": "admin@example.com",
        "password": "AdminPass123!"
    })
    csrf = login_res.json()["csrf_token"]
    headers = {"X-CSRF-Token": csrf} if csrf else {}

    # Deactivate test_user
    deactivate_res = client.patch(
        f"/api/admin/users/{test_user.id}/status",
        headers=headers,
        json={"is_active": False}
    )
    assert deactivate_res.status_code == 200
    assert deactivate_res.json()["is_active"] is False

    db_session.refresh(test_user)
    assert test_user.is_active is False

    # Prevent admin from deactivating themselves
    self_res = client.patch(
        f"/api/admin/users/{test_admin.id}/status",
        headers=headers,
        json={"is_active": False}
    )
    assert self_res.status_code == 400
    assert "cannot deactivate their own accounts" in self_res.json()["detail"]


def test_admin_update_user_role(client, test_admin, test_user, db_session):
    login_res = client.post("/api/auth/login", json={
        "email": "admin@example.com",
        "password": "AdminPass123!"
    })
    csrf = login_res.json()["csrf_token"]
    headers = {"X-CSRF-Token": csrf} if csrf else {}

    # Elevate test_user to admin
    role_res = client.patch(
        f"/api/admin/users/{test_user.id}/role",
        headers=headers,
        json={"role": "admin"}
    )
    assert role_res.status_code == 200
    assert role_res.json()["role"] == "admin"

    db_session.refresh(test_user)
    assert test_user.role == "admin"

    # Prevent admin from demoting themselves
    self_res = client.patch(
        f"/api/admin/users/{test_admin.id}/role",
        headers=headers,
        json={"role": "user"}
    )
    assert self_res.status_code == 400
    assert "cannot demote their own role" in self_res.json()["detail"]
