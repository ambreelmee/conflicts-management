from flask import abort, request
import requests


def validate_token(access_token):
    '''Verifies that an access-token is valid
    Returns a boolean'''
    headers = {'Authorization':  access_token}
    proxyDict = {"http": "10.244.16.9:9090"}
    url = 'https://data-esr-authentification.herokuapp.com/api/check_token'
    r = requests.post(url, proxies=proxyDict, headers=headers)
    return r.status_code == 200


def authorized(fn):
    """Decorator that checks that requests
    contain an access-token in the request header.
    """

    def _wrap(*args, **kwargs):
        if 'Authorization' not in request.headers:
            # Unauthorized
            print("No token in header")
            abort(401)
            return None
        authorized = validate_token(request.headers['Authorization'])
        if not authorized:
            # Unauthorized
            abort(401)
            return None

        return fn(*args, **kwargs)
    return _wrap
