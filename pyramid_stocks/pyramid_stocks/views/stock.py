from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound, HTTPNotFound, HTTPBadRequest
from pyramid.security import NO_PERMISSION_REQUIRED
from sqlalchemy.exc import DBAPIError
from ..models import Account
from ..models import Stock

import requests
from . import db_err_msg
from . import IEX_API_URL

@view_config(route_name='stock', renderer='../templates/stock-add.jinja2')
def stock_view(request):
    '''View to search for stocks
    GET shows a search bar and optionally details of a stock
    POST puts a searched stock into a user's portfolio
    '''

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
        except:
            return HTTPNotFound()
        
        data = response.json()
        q_account = request.dbsession.query(Account)
        q_stock = request.dbsession.query(Stock)
        user = q_account.filter(Account.username==request.authenticated_userid).first()

        try:
            # Try to update an existing record
            record = q_stock.filter(Stock.symbol==symbol).first()
            record.symbol = data['symbol']
            record.companyName = data['companyName']
            record.exchange = data['exchange']
            record.industry = data['industry']
            record.website = data['website']
            record.description = data['description']
            record.CEO = data['CEO']
            record.issueType = data['issueType']
            record.sector = data['sector']
            user.stock_id.append(record)

        except AttributeError:
            # If record doesn't exist, add a new record and update junction table
            request.dbsession.add(Stock(**data))
            new_record = q_stock.filter(Stock.symbol==data['symbol']).first()
            user.stock_id.append(new_record)

        return HTTPFound(location=request.route_url('portfolio'))
