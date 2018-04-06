from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from sqlalchemy.exc import DBAPIError
from ..sample_data import MOCK_DATA
from ..models import MyModel


@view_config(route_name='home', renderer='../templates/index.jinja2')
def home_view(request):
    return {}


@view_config(route_name='auth', renderer='../templates/auth.jinja2')
def auth_view(request):
    if request.method == 'GET':
        try:
            username = request.GET['username']
            password = request.GET['password']

            return HTTPFound(location=request.route_url('portfolio'))

        except KeyError:
            return {}

        return HTTPFound(location=request.route_url('portfolio'))
    
    if request.method == 'POST':
        try:
            username = request.POST['username']
            password = request.POST['password']
        except KeyError:
            return HTTPNotFound()

        return HTTPFound(location=request.route_url('portfolio'))

    return HTTPNotFound()


@view_config(route_name='stock', renderer='../templates/stock-add.jinja2')
def stock_view(request):
    return {}


@view_config(route_name='portfolio', renderer='../templates/portfolio.jinja2')
def portfolio_view(request):
    if request.method == 'GET':
        return {'mock_data' : MOCK_DATA}
    return HTTPNotFound()

@view_config(route_name='stock-detail', renderer='../templates/stock-detail.jinja2')
def stock_detail_view(request):
    try:
        symbol = request.matchdict['symbol']
    except KeyError:
        return HTTPNotFound()

    for company in MOCK_DATA:
        if company['symbol'] == symbol:
            return {'company': company}

    return HTTPNotFound()


db_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_pyramid_stocks_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""
