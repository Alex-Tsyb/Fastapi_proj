from unittest.mock import MagicMock, patch

import pytest

from src.database.models import User
from src.services.auth import auth_service


@pytest.fixture()
def token(client, user, session, monkeypatch):
    mock_send_email = MagicMock()
    monkeypatch.setattr("src.routes.auth.send_email", mock_send_email)
    client.post("/api/auth/signup", json=user)
    current_user: User = session.query(User).filter(User.email == user.get('email')).first()
    current_user.confirmed = True
    session.commit()
    response = client.post(
        "/api/auth/login",
        data={"username": user.get('email'), "password": user.get('password')},
    )
    data = response.json()
    return data["access_token"]


def test_create_contact(client, token):
    with patch.object(auth_service, 'get_password_hash') as r_mock:
        r_mock.get.return_value = None
        response = client.post(
            "/api/contacts",
            json={
                "name": "Bob",
                "surname": "Dylon",
                "email": "Bob85@gmail.com",
                "phone": "7777777777",
                "birthday": "1985-07-25",
                "additional": "Some info"
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 201, response.text
        data = response.json()
        assert data["name"] == "Bob"


def test_get_contact(client, token):
    with patch.object(auth_service, 'get_password_hash') as r_mock:
        r_mock.get.return_value = None
        response = client.get(
            "/api/contacts/1",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["name"] == "Bob"


def test_get_contact_not_found(client, token):
    with patch.object(auth_service, 'get_password_hash') as r_mock:
        r_mock.get.return_value = None
        response = client.get(
            "/api/contacts/2",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 404, response.text
        data = response.json()
        assert data["detail"] == "Contact not found"


def test_update_contact(client, token):
    with patch.object(auth_service, 'get_password_hash') as r_mock:
        r_mock.get.return_value = None
        response = client.put(
            "/api/contacts/1",
            json={
                "name": "Iggy",
                "surname": "",
                "email": "Iggy87@gmail.com",
                "phone": "88888888",
                "birthday": "1987-08-27",
                "additional": "Some new info"
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["name"] == "Iggy"


def test_update_contact_not_found(client, token):
    with patch.object(auth_service, 'get_password_hash') as r_mock:
        r_mock.get.return_value = None
        response = client.put(
            "/api/contacts/2",
            json={
                "name": "Iggy",
                "surname": "",
                "email": "Iggy87@gmail.com",
                "phone": "88888888",
                "birthday": "1987-08-27",
                "additional": "Some new info"
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 404, response.text
        data = response.json()
        assert data["detail"] == "Contact not found"


def test_delete_contact(client, token):
    with patch.object(auth_service, 'get_password_hash') as r_mock:
        r_mock.get.return_value = None
        response = client.delete(
            "/api/contacts/1",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["name"] == "Iggy"


def test_repeat_delete_contact(client, token):
    with patch.object(auth_service, 'get_password_hash') as r_mock:
        r_mock.get.return_value = None
        response = client.delete(
            "/api/contacts/1",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 404, response.text
        data = response.json()
        assert data["detail"] == "Contact not found"