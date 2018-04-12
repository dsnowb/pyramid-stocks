from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound, HTTPNotFound, HTTPBadRequest, HTTPUnauthorized
from pyramid.security import NO_PERMISSION_REQUIRED, remember, forget
from sqlalchemy.exc import DBAPIError, IntegrityError
from ..models import Account
from . import db_err_msg

@view_config(
    route_name='auth',
    renderer='../templates/auth.jinja2',
    permission=NO_PERMISSION_REQUIRED
    )
def auth_view(request):
    if request.method == 'GET':
        try:
            username = request.GET['username']
            password = request.GET['password']
        except KeyError:
            return {}

        is_authenticated = Account.check_credentials(request, username, password)
        if is_authenticated[0]:
            headers = remember(request, userid=username)
            return HTTPFound(location=request.route_url('portfolio'), headers=headers)
        else:
            return HTTPUnauthorized()
    
    if request.method == 'POST':
        try:
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
        except KeyError:
            return HTTPBadRequest()

        instance = Account(
                username=username,
                email=email,
                password=password,
        )

        headers = remember(request, userid=instance.username)

        try:
            request.dbsession.add(instance)
            request.dbsession.flush()

        except IntegrityError:
            return Response(db_err_msg, content_type='text/plain', status=500)

        except DBAPIError:
            return Response(db_err_msg, content_type='text/plain', status=500)

        return HTTPFound(location=request.route_url('portfolio'), headers=headers)


    return HTTPFound(location=request.route_url('home'))
