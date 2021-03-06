import pytest
import app


@pytest.fixture
def client():
    with app.app.test_client() as client:
        yield client


def test_integration_response(client):
    rv = client.get("/")
    assert b"DMIA" in rv.data


def test_unit_unpopular_password():
    popularity = app.password_model.predict("gkdfjng")
    assert popularity < 2


def test_unit_popular_password():
    popularity = app.password_model.predict("123")
    assert popularity > 15
