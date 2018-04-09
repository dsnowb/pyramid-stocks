from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound, HTTPNotFound, HTTPBadRequest
from sqlalchemy.exc import DBAPIError
from ..sample_data import MOCK_DATA
from ..models import Account
from ..models import Stock
import requests

IEX_API_URL = 'https://api.iextrading.com/1.0'

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


@view_config(route_name='portfolio', renderer='../templates/portfolio.jinja2')
def portfolio_view(request):
    if request.method == 'GET':
        try:
            query = request.dbsession.query(Stock)
            all_entries = query.all()
        except DBAPIError:
            return DBAPIError(db_err_msg, content_type='text/plain', status=500)

        return {'companies': all_entries}

    return HTTPNotFound()


@view_config(route_name='stock', renderer='../templates/stock-add.jinja2')
def stock_view(request):
    if request.method == 'GET':
        try:
            symbol = request.GET['symbol']
        except KeyError:
            return {}

        response = requests.get('{}/stock/{}/company'.format(IEX_API_URL, symbol))
        try:
            company = response.json()
        except:
            return {}
        
        response = requests.get('{}/stock/{}/time-series'.format(IEX_API_URL, symbol))
        time_series = response.json()
        rev_ts = []
        for i in range(len(time_series) - 1,-1,-1):
            rev_ts.append(time_series[i])
        return {'company': company, 'time_series': rev_ts}

    if request.method == 'POST':
        try:
            symbol = request.POST['symbol']
        except KeyError:
            return HTTPBadRequest()

        try:
            response = requests.get('{}/stock/{}/company'.format(IEX_API_URL, symbol))
            response = response.json()
        except:
            return HTTPNotFound()

        query = request.dbsession.query(Stock)
        try:
            record = query.filter(Stock.symbol==symbol).first()
            record.symbol = response['symbol']
            record.companyName = response['companyName']
            record.exchange = response['exchange']
            record.industry = response['industry']
            record.website = response['website']
            record.description = response['description']
            record.CEO = response['CEO']
            record.issueType = response['issueType']
            record.sector = response['sector']

        except KeyError:     
            request.dbsession.add(Stock(**response))

        return HTTPFound(location=request.route_url('portfolio'))
       

@view_config(route_name='stock-detail', renderer='../templates/stock-detail.jinja2')
def stock_detail_view(request):
    try:
        symbol = request.matchdict['symbol']
    except KeyError:
        return HTTPNotFound()

    try:
        query = request.dbsession.query(Stock)
    
    except DBAPIError:
        return DBAPIError(db_err_msg, content_type='text/plain', status=500)

    for company in query.all():
        if company.symbol == symbol:
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
