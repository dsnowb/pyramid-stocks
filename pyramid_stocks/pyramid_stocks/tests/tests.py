def test_home_view(dummy_request):
    from ..views.default import home_view
    assert home_view(dummy_request) == {}

def test_auth_view(dummy_request):
    from ..views.auth import auth_view
    assert auth_view(dummy_request) == {}

def test_stock_view(dummy_request):
    from ..views.default import stock_view
    assert stock_view(dummy_request) == {}

def test_home_view_post(dummy_post_request):
    from ..views.default import home_view
    assert home_view(dummy_post_request) == {}

def test_auth_view_post_no_params(dummy_post_request):
    from pyramid.httpexceptions import HTTPBadRequest
    from ..views.auth import auth_view
    assert isinstance(auth_view(dummy_post_request), HTTPBadRequest)

def test_stock_view_post(dummy_post_request):
    from pyramid.httpexceptions import HTTPBadRequest
    from ..views.default import stock_view
    assert isinstance(stock_view(dummy_post_request), HTTPBadRequest)

def test_portfolio_view_post(dummy_post_request):
    from pyramid.httpexceptions import HTTPNotFound
    from ..views.default import portfolio_view
    assert isinstance(portfolio_view(dummy_post_request),HTTPNotFound)

def test_portfolio_view(dummy_request):
    from ..views.default import portfolio_view
    assert 'companies' in portfolio_view(dummy_request).keys()

def test_stock_detail_view_post(dummy_post_request):
    from pyramid.httpexceptions import HTTPNotFound
    from ..views.default import portfolio_view
    assert isinstance(portfolio_view(dummy_post_request),HTTPNotFound)

def test_stock_view(dummy_request):
    from ..views.default import stock_view
    dummy_request.GET = {'symbol':'GE'}
    stock_view(dummy_request)['company'] == 'GE'
'''
def test_stock_view_post(dummy_request, db_session):
    from ..views.default import stock_view
    from pyramid.httpexceptions import HTTPFound
    dummy_request.method = 'POST'
    dummy_request.POST = {'symbol':'ge'}
    assert isinstance(stock_view(dummy_request), HTTPFound)
'''
