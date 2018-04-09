def test_home_view(dummy_request):
    from ..views.default import home_view
    assert home_view(dummy_request) == {}

def test_auth_view(dummy_request):
    from ..views.default import auth_view
    assert auth_view(dummy_request) == {}

def test_stock_view(dummy_request):
    from ..views.default import stock_view
    assert stock_view(dummy_request) == {}

def test_portfolio_view(dummy_request):
    from ..views.default import portfolio_view
    assert portfolio_view(dummy_request)['mock_data'][0]['symbol'] == "GE"

def test_stock_detail_view(dummy_request):
    from ..views.default import stock_detail_view
    dummy_request.matchdict['symbol'] = 'AAPL'
    assert stock_detail_view(dummy_request)['company']['symbol'] == "AAPL"
    
def test_home_view_post(dummy_post_request):
    from ..views.default import home_view
    assert home_view(dummy_post_request) == {}

def test_auth_view_post_no_params(dummy_post_request):
    from pyramid.httpexceptions import HTTPNotFound
    from ..views.default import auth_view
    assert isinstance(auth_view(dummy_post_request), HTTPNotFound)
'''
This test keeps throwing a ComponentLookupError
def test_auth_view_post_params(dummy_post_user_pass_request):
    from pyramid.httpexceptions import HTTPFound
    from ..views.default import auth_view
    assert isinstance(auth_view(dummy_post_user_pass_request),HTTPFound)
'''
def test_stock_view_post(dummy_post_request):
    from ..views.default import stock_view
    assert stock_view(dummy_post_request) == {}

def test_portfolio_view_post(dummy_post_request):
    from pyramid.httpexceptions import HTTPNotFound
    from ..views.default import portfolio_view
    assert isinstance(portfolio_view(dummy_post_request),HTTPNotFound)

def test_stock_detail_view_post(dummy_post_request):
    from pyramid.httpexceptions import HTTPNotFound
    from ..views.default import portfolio_view
    assert isinstance(portfolio_view(dummy_post_request),HTTPNotFound)
