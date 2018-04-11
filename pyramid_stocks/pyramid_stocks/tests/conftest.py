import pytest
from pyramid import testing
from ..models.meta import Base
from ..models import Account
from ..models import Stock

@pytest.fixture
def dummy_post_request():
    return testing.DummyRequest(method="POST")

@pytest.fixture
def dummy_post_user_pass_request():
    return testing.DummyRequest(method="POST", post={'username':'A', 'password':'B'})

@pytest.fixture
def test_stock():
    return Stock(
        symbol='FAKE',
        companyName='Fake Co.',
        CEO='Mr. Fakerson',
    )

@pytest.fixture
def test_account():
    return Account(
            username='MrFake',
            email='supsup@sup.com',
    )

@pytest.fixture
def configuration(request):
    """Setup a database for testing purposes."""
    config = testing.setUp(settings={
        'sqlalchemy.url': 'postgres://localhost:5432/pyramid_stocks_test'
    })
    config.include('..models')
    config.include('..routes')

    def teardown():
        testing.tearDown()

    request.addfinalizer(teardown)
    return config


@pytest.fixture
def db_session(configuration, request):
    """Create a database session for interacting with the test database."""
    SessionFactory = configuration.registry['dbsession_factory']
    session = SessionFactory()
    engine = session.bind
    Base.metadata.create_all(engine)

    def teardown():
        session.transaction.rollback()
        Base.metadata.drop_all(engine)

    request.addfinalizer(teardown)
    return session


@pytest.fixture
def dummy_request(db_session):
    """Create a dummy GET request with a dbsession."""
    return testing.DummyRequest(dbsession=db_session)
