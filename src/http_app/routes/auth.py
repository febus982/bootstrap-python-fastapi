from typing import Annotated, Optional

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, SecurityScopes

from common import AppConfig
from http_app.dependencies import get_app_config


class MissingAuthorizationServerException(HTTPException):
    def __init__(self, **kwargs):
        super().__init__(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Authorization server not available",
        )


class UnauthorizedException(HTTPException):
    def __init__(self, detail: str, **kwargs):
        super().__init__(status.HTTP_403_FORBIDDEN, detail=detail)


class UnauthenticatedException(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail="Requires authentication")


def _jwks_client(config: Annotated[AppConfig, Depends(get_app_config)]) -> jwt.PyJWKClient:
    if not config.AUTH.JWKS_URL:
        raise MissingAuthorizationServerException()
    return jwt.PyJWKClient(config.AUTH.JWKS_URL)


async def decode_jwt(
    security_scopes: SecurityScopes,
    config: AppConfig = Depends(get_app_config),
    jwks_client: jwt.PyJWKClient = Depends(_jwks_client),
    token: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer()),
):
    if token is None:
        raise UnauthenticatedException()

    try:
        signing_key = jwks_client.get_signing_key_from_jwt(token.credentials).key
    except jwt.exceptions.PyJWKClientError as error:
        raise UnauthorizedException(str(error))
    except jwt.exceptions.DecodeError as error:
        raise UnauthorizedException(str(error))

    try:
        # TODO: Review decode setup and verifications
        #       https://pyjwt.readthedocs.io/en/stable/api.html#jwt.decode
        payload = jwt.decode(
            jwt=token.credentials,
            key=signing_key,
            algorithms=[config.AUTH.JWT_ALGORITHM],
        )
    except Exception as error:
        raise UnauthorizedException(str(error))

    return payload
