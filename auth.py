"""Authorization code for app.

Defines decorator @requires_auth(permission="") and helper function has_permission()"""

import json
from functools import wraps
from urllib.request import urlopen
import os

from jose import jwt
from flask import request, abort

AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")
ALGORITHMS = ['RS256']
API_AUDIENCE = os.environ.get("API_AUDIENCE")

## AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


## Auth Header
'''
@TODO implement get_token_auth_header() method
'''
def get_token_auth_header():
    auth = request.headers.get('Authorization', None)
    if not auth:
        raise AuthError({
            'code': 'authorization_header_missing',
            'description': 'Missing expected HTTP-Header (Authorization).'
            }, 401)

    parts = auth.split()
    if parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must start with "bearer".'
            }, 401)

    elif len(parts) == 1:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Token not found.'
            }, 401)

    elif len(parts) > 2:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must be a bearer token.  (Too many parts detected.)'
            }, 401)
    token = parts[1]
    return token

'''
@TODO implement check_permissions(permission, payload) method
'''
def check_permissions(permission, payload):
    if "permissions" not in payload:
        abort(401)

    if permission not in payload['permissions']:
        abort(403)

    return True

'''
@TODO implement verify_decode_jwt(token) method
'''
def verify_decode_jwt(token):
    # Verification boilerplate
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed (lacking "kid" attribute).'
            }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer=f'https://{AUTH0_DOMAIN}/')

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
                }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please check the audience and issuer.'
                }, 401)

        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
                }, 400)
    raise AuthError({
        'code': 'invalid_header',
        'description': 'Authentication token did not contain an appropriate RSA key.'
        }, 401)


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                token = get_token_auth_header()
                payload = verify_decode_jwt(token)
            except:
                abort(401)

            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator

def has_permission(permission=''):
    try:
        token = get_token_auth_header()
        payload = verify_decode_jwt(token)
    except:
        abort(401)

    return check_permissions(permission, payload)
