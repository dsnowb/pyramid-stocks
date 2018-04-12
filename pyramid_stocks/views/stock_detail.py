from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotFound
from sqlalchemy.exc import DBAPIError
from ..models import Stock
from . import db_err_msg


@view_config(route_name='stock-detail', renderer='../templates/stock-detail.jinja2')
def stock_detail_view(request):
    '''View a stock in detail. GET only.'''

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
