from pyramid.view import forbidden_view_config
from pyramid.httpexceptions import HTTPFound

@forbidden_view_config()
def forbidden_view(request):
    '''Redirect to auth view if forbidden'''
    return HTTPFound(location=request.route_url('auth'))
