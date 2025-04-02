import pytest
from first_part.superhero_first import get_tallest_hero


class MockResponse:
    def __init__(self, json_data):
        self.json_data = json_data

    def json(self):
        return self.json_data

    def raise_for_status(self):
        pass


@pytest.fixture
def mock_heroes():
    return [
        {
            "name": "Hero1",
            "appearance": {"gender": "Male", "height": ["180 cm"]},
            "work": {"occupation": "Hero"}
        },
        {
            "name": "Hero2",
            "appearance": {"gender": "Male", "height": ["190"]},
        }
    ]


def test_male_with_work(monkeypatch, mock_heroes):
    def mock_get(*args, **kwargs):
        return MockResponse(mock_heroes)

    monkeypatch.setattr('requests.get', mock_get)

    result = get_tallest_hero("Male", True)
    assert result == ("Hero1", 180.0)


def test_male_without_work(monkeypatch, mock_heroes):
    def mock_get(*args, **kwargs):
        return MockResponse(mock_heroes)

    monkeypatch.setattr('requests.get', mock_get)

    result = get_tallest_hero("Male", False)
    assert result == ("Hero2", 190.0)


def test_no_matches(monkeypatch):
    def mock_get(*args, **kwargs):
        return MockResponse([])

    monkeypatch.setattr('requests.get', mock_get)

    result = get_tallest_hero("Female", True)
    assert result is None