def test_default_response_auth_view(dummy_request):
    from ..views.auth import auth_view

    response = auth_view(dummy_request)
    assert response == {}


def test_auth_signin_view(dummy_request):
    from ..views.auth import auth_view
    from pyramid.httpexceptions import HTTPUnauthorized

    dummy_request.GET = {'username': 'bob', 'password': 'bob'}
    response = auth_view(dummy_request)
    assert response.status_code == 401
    assert isinstance(response, HTTPUnauthorized)


def test_auth_signup_view(dummy_request):
    from ..views.auth import auth_view
    from pyramid.httpexceptions import HTTPFound

    dummy_request.POST = {'username': 'bob', 'password': 'bob', 'email': 'bob@bob.com'}
    dummy_request.method = 'POST'
    response = auth_view(dummy_request)
    assert response.status_code == 302
    assert isinstance(response, HTTPFound)


def test_bad_reqeust_auth_signup_view(dummy_request):
    from ..views.auth import auth_view
    from pyramid.httpexceptions import HTTPBadRequest

    dummy_request.POST = {'password': 'bob', 'email': 'bob@bob.com'}
    dummy_request.method = 'POST'
    response = auth_view(dummy_request)
    assert response.status_code == 400
    assert isinstance(response, HTTPBadRequest)


def test_bad_request_method_auth_signup_view(dummy_request):
    from ..views.auth import auth_view
    from pyramid.httpexceptions import HTTPFound

    dummy_request.POST = {'password': 'bob', 'email': 'bob@bob.com'}
    dummy_request.method = 'PUT'
    response = auth_view(dummy_request)
    assert response.status_code == 302
    assert isinstance(response, HTTPFound)
