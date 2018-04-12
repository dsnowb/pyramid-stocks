from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound, HTTPNotFound, HTTPBadRequest
from sqlalchemy.exc import DBAPIError
from ..models import Account
from ..models import Stock

import requests
from . import db_err_msg
from . import IEX_API_URL
from pyramid.security import NO_PERMISSION_REQUIRED


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
