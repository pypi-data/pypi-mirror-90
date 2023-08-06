"""Supplies authentication functions."""
import ioc.exc
from fastapi import Cookie
from fastapi import Depends
from fastapi import Request
from unimatrix.ext import crypto
from unimatrix.ext import jose

from .exceptions import BearerTokenMissing
from .exceptions import InvalidAuthorizationScheme
from .exceptions import BearerTokenUnverifiable


def get_bearer_token(request: Request):
    header = request.headers.get('Authorization')
    value = None
    if header:
        scheme, _, value = str.partition(header, ' ')
        if str.lower(scheme) != 'bearer':
            raise InvalidAuthorizationScheme(scheme, ['Bearer'])
    return value


def Session(name, enabled=False):
    if not enabled:
        return Depends(lambda: None)

    async def f(request: Request, sessionid: str = Cookie(None, alias=name)):
        return request.cookies.get(name)

    return Depends(f)


def RequestClaims(allow_cookies=False, cookie_name='session', required=True):
    session = Session(cookie_name, allow_cookies)
    async def f(request: Request, bearer=Bearer, sessionid:str=session):
        if not bearer and allow_cookies:
            bearer = sessionid
        if not bearer and required:
            raise BearerTokenMissing

        if bearer:
            try:
                return await jose.payload(str.encode(bearer))
            except ioc.exc.UnsatisfiedDependency:
                raise
            except (crypto.Signature.InvalidSignature, LookupError):
                if required:
                    raise BearerTokenUnverifiable

    return Depends(f)


Bearer = Depends(get_bearer_token)
