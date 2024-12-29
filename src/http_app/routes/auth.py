import time
from typing import Annotated, Any, Optional

import jwt
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from common import AppConfig
from http_app.dependencies import app_config


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
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Requires authentication"
        )


def _jwks_client(config: Annotated[AppConfig, Depends(app_config)]) -> jwt.PyJWKClient:
    if not config.AUTH.JWKS_URL:
        raise MissingAuthorizationServerException()
    return jwt.PyJWKClient(config.AUTH.JWKS_URL)


class JWTBearer(HTTPBearer):
    async def __call__(
        self,
        request: Request,
    ) -> Optional[HTTPAuthorizationCredentials]:
        credentials = await super(JWTBearer, self).__call__(request)

        await self.decode(request)

        return credentials

    async def decode(
        self,
        request: Request,
        jwks_client: jwt.PyJWKClient = Depends(_jwks_client),
        config: AppConfig = Depends(app_config),
    ) -> dict[str, Any]:
        credentials = await super(JWTBearer, self).__call__(request)

        if not credentials:
            raise UnauthenticatedException()

        if not credentials.scheme == "Bearer":
            raise UnauthorizedException("Invalid authentication scheme.")

        try:
            signing_key = jwks_client.get_signing_key_from_jwt(
                credentials.credentials
            ).key
        except jwt.exceptions.PyJWKClientError as error:
            raise UnauthorizedException(str(error))
        except jwt.exceptions.DecodeError as error:
            raise UnauthorizedException(str(error))

        try:
            # TODO: Review decode setup and verifications
            #       https://pyjwt.readthedocs.io/en/stable/api.html#jwt.decode
            payload = jwt.decode(
                jwt=credentials.credentials,
                key=signing_key,
                algorithms=[config.AUTH.JWT_ALGORITHM],
            )
        except Exception as error:
            raise UnauthorizedException(str(error))

        return payload
