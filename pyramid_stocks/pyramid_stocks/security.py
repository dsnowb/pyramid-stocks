from pyramid.security import Allow, Everyone, Authenticated
from pyramid.session import SignedCookieSessionFactory
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy


class Root:
    def __init__(self, request):
        self.request = request

    __acl__ = [
            (Allow, Everyone, 'view'),
            (Allow, Authenticated, 'secret'),
    ]

def includeme(config):
    authz_policy = ACLAuthorizationPolicy()
    authn_policy = AuthTktAuthenticationPolicy(
        secret='mysecret',
        hashalg='sha512',
    )
    session_factory = SignedCookieSessionFactory('anothersecret')

    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)
    config.set_default_permission('secret')
    config.set_root_factory(Root)
    config.set_session_factory(session_factory)
    config.set_default_csrf_options(require_csrf=True)
