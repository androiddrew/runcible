# TODO remove user creatation at this endpoint. Users
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


# TODO based on this app. You would not share other user information. deprecate and replace with a login protected /auth/profile endpoint.
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


# TODO remove this end point from code
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


def test_registration(client):
    payload = {
        "email": "test@runcible.io",
        "display_name": "test_user",
        "password": "password",
    }
    response = client.post("/auth/register", json=payload)
    content = response.json()
    assert response.status_code == 201
    assert content.get("email") == payload.get("email")
    assert content.get("display_name") == payload.get("display_name")
    assert response.headers.get_all("location") is not None


def test_user_registration_with_already_used_email(client):
    payload = {
        "email": "test2@runcible.io",
        "display_name": "test2_user",
        "password": "password",
    }
    response = client.post("/auth/register", json=payload)
    assert response.status_code == 201
    conflict_response = client.post("/auth/register", json=payload)
    assert conflict_response.status_code == 409


def test_registration_fails_when_email_is_not_valid(client):
    payload = {
        "email": "test2@notemail",
        "display_name": "test2_user",
        "password": "password",
    }
    response = client.post("/auth/register", json=payload)
    assert response.status_code == 400


def test_failed_login_of_user_that_exists(client):
    user_payload = {
        "email": "test@runcible.io",
        "display_name": "test_user",
        "password": "password",
    }
    client.post("/auth/register", json=user_payload)
    login_payload = {"email": "test@runcible.io", "password": "notthepassword"}
    response = client.post("/auth/login", json=login_payload)
    assert response.status_code == 401
    content = response.json()
    assert content["status"] == 401
    assert content["message"] == "Password provided does not match."


def test_failed_login_of_user_that_does_not_exist(client):
    payload = {"email": "notauser@runcible.io", "password": "password"}
    response = client.post("/auth/login", json=payload)
    assert response.status_code == 404
    content = response.json()
    assert content["status"] == 404
    assert content["message"] == "User: notauser@runcible.io does not exist"


def test_user_login(client):
    user_payload = {
        "email": "test@runcible.io",
        "display_name": "test_user",
        "password": "password",
    }
    client.post("/auth/register", json=user_payload)
    payload = {"email": "test@runcible.io", "password": "password"}
    response = client.post("/auth/login", json=payload)
    assert response.status_code == 200
    content = response.json()
    assert content["auth_token"]
    assert content["status"] == 200
    assert content["message"] == "Successfully logged in."


def test_user_profile_from_jwt(client):
    user_payload = {
        "email": "test@runcible.io",
        "display_name": "test_user",
        "password": "password",
    }
    client.post("/auth/register", json=user_payload)
    login_response = client.post("/auth/login", json={"email": "test@runcible.io", "password": "password"})
    token = login_response.json().get('auth_token')
    profile_response = client.get("/auth/profile", headers={"Authorization": f"Bearer {token}"})
    assert profile_response.status_code == 200
    profile_content = profile_response.json()
    assert profile_content["display_name"] == "test_user"
    assert profile_content["email"] == "test@runcible.io"
    assert profile_content["confirmed"] == False
