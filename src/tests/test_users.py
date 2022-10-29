import json

from src.api.models import User


def test_add_user(test_app, test_database):
    client = test_app.test_client()
    res = client.post(
        "/users",
        data=json.dumps({"username": "alex", "email": "alex@kali.com"}),
        content_type="application/json",
    )
    data = json.loads(res.data.decode())

    assert res.status_code == 201
    assert "alex@kali.com was added!" in data["message"]


def test_add_user_invalid_json(test_app, test_database):
    client = test_app.test_client()
    res = client.post("/users", data=json.dumps({}), content_type="application/json")
    data = json.loads(res.data.decode())

    assert res.status_code == 400
    assert "Input payload validation failed" in data["message"]


def test_add_user_invalid_json_keys(test_app, test_database):
    client = test_app.test_client()
    res = client.post(
        "/users",
        data=json.dumps({"email": "joy@eskrima.com"}),
        content_type="application/json",
    )
    data = json.loads(res.data.decode())

    assert res.status_code == 400
    assert "Input payload validation failed" in data["message"]


def test_add_user_duplicate_email(test_app, test_database):
    client = test_app.test_client()
    client.post(
        "/users",
        data=json.dumps({"username": "alex", "email": "alex@kali.com"}),
        content_type="application/json",
    )
    res = client.post(
        "/users",
        data=json.dumps({"username": "alex", "email": "alex@kali.com"}),
        content_type="application/json",
    )
    data = json.loads(res.data.decode())

    assert res.status_code == 400
    assert "Sorry. That email already exists." in data["message"]


def test_single_user(test_app, test_database, add_user):
    user = add_user("randy", "randy@arnis.com")
    client = test_app.test_client()
    res = client.get(f"/users/{user.id}")
    data = json.loads(res.data.decode())

    assert res.status_code == 200
    assert "randy" in data["username"]
    assert "randy@arnis.com" in data["email"]


def test_single_user_incorrect_id(test_app, test_database):
    client = test_app.test_client()
    res = client.get("/users/999")
    data = json.loads(res.data.decode())

    assert res.status_code == 404
    assert "User 999 does not exist" in data["message"]


def test_all_users(test_app, test_database, add_user):
    test_database.session.query(User).delete()
    add_user("leila", "leila@eskrima.com")
    add_user("kristian", "kristian@arnis.com")
    client = test_app.test_client()
    res = client.get("/users")
    data = json.loads(res.data.decode())

    assert res.status_code == 200
    assert len(data) == 2
    assert "leila" in data[0]["username"]
    assert "leila@eskrima.com" in data[0]["email"]
    assert "kristian" in data[1]["username"]
    assert "kristian@arnis.com" in data[1]["email"]
