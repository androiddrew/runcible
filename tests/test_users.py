def test_user_create(client):
    user = {
        "email": "someone@email.com,",
        "display_name": "lauraleah",
        "password": "mypassword",
    }
    response = client.post("/users", json=user)
    content = response.json()
    assert response.status_code == 201
    assert content.get("email") == user.get("email")
    assert content.get("display_name") == user.get("display_name")
    assert response.headers.get_all("location") is not None


def test_get_user_by_display_name(client):
    user = {
        "email": "dirp@email.com,",
        "display_name": "anyone",
        "password": "mypassword",
    }
    create_response = client.post("/users", json=user)
    assert create_response.status_code == 201
    response = client.get("/users/anyone")
    content = response.json()
    assert response.status_code == 200
    assert content.get("email") == user.get("email")
    assert content.get("display_name") == user.get("display_name")


def test_user_create_with_already_used_email(client):
    user = {
        "email": "drew@email.com,",
        "display_name": "drew",
        "password": "mypassword",
    }
    response = client.post("/users", json=user)
    assert response.status_code == 201
    dup_user_response = client.post("/users", json=user)
    assert dup_user_response.status_code == 409
