import pytest


@pytest.fixture
def empty_string() -> str:
    return ""


@pytest.fixture
def card_number() -> str:
    return "4608837868705199"


@pytest.fixture
def account_number() -> str:
    return "64686473678894770123"
