import pytest
from pyramid import testing

@pytest.fixture
def dummy_request():
    return testing.DummyRequest()

@pytest.fixture
def dummy_post_request():
    return testing.DummyRequest(method="POST")

@pytest.fixture
def dummy_post_user_pass_request():
    return testing.DummyRequest(method="POST", post={'username':'A', 'password':'B'})
