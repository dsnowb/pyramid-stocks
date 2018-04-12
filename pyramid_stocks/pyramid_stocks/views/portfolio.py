from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotFound
from sqlalchemy.exc import DBAPIError
from ..models import Account
from . import db_err_msg

@view_config(route_name='portfolio', renderer='../templates/portfolio.jinja2')
def portfolio_view(request):
    if request.method == 'GET':
        try:
            q = request.dbsession.query(Account)
            user = q.filter(Account.username==request.authenticated_userid).first()
        except DBAPIError:
            return DBAPIError(db_err_msg, content_type='text/plain', status=500)

        print('USER: {}'.format(user))

        return {'companies': user.stock_id}

    return HTTPNotFound()
