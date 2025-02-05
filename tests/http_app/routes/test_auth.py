from unittest.mock import MagicMock, patch

import pytest
from fastapi.security import HTTPAuthorizationCredentials, SecurityScopes
from jwt import PyJWK, PyJWKClient
from jwt.exceptions import DecodeError, PyJWKClientError

from common import AppConfig
from common.config import AuthConfig
from http_app.routes.auth import (
    MissingAuthorizationServerException,
    UnauthenticatedException,
    UnauthorizedException,
    _jwks_client,
    decode_jwt,
)


def test_jwks_client_raises_without_jwks_url():
    with pytest.raises(MissingAuthorizationServerException):
        _jwks_client(config=AppConfig(AUTH=AuthConfig(JWKS_URL=None)))


def test_jwks_client_returns_a_client_with_jwks_url():
    result = _jwks_client(config=AppConfig(AUTH=AuthConfig(JWKS_URL="http://test.com")))
    assert isinstance(result, PyJWKClient)


async def test_decode_jwt_raises_without_token():
    with pytest.raises(UnauthenticatedException):
        await decode_jwt(
            security_scopes=SecurityScopes(),
            config=AppConfig(),
            jwks_client=MagicMock(),
            token=None,
        )


@pytest.mark.parametrize("exception", (PyJWKClientError, DecodeError))
async def test_decode_jwt_raises_if_jwks_client_fails(exception):
    mock_jwks_client = MagicMock(spec=PyJWKClient)
    mock_jwks_client.get_signing_key_from_jwt = MagicMock(side_effect=exception)
    with pytest.raises(UnauthorizedException):
        await decode_jwt(
            security_scopes=SecurityScopes(),
            config=AppConfig(),
            jwks_client=mock_jwks_client,
            token=HTTPAuthorizationCredentials(scheme="bearer", credentials="some_token"),
        )


async def test_decode_jwt_raises_if_decode_fails():
    returned_key = MagicMock(spec=PyJWK)
    returned_key.key = "some_key"
    mock_jwks_client = MagicMock(spec=PyJWKClient)
    mock_jwks_client.get_signing_key_from_jwt = MagicMock(return_value=returned_key)

    with pytest.raises(UnauthorizedException):
        await decode_jwt(
            security_scopes=SecurityScopes(),
            config=AppConfig(),
            jwks_client=mock_jwks_client,
            token=HTTPAuthorizationCredentials(
                # The token cannot be decrypted and will trigger the exception
                scheme="bearer",
                credentials="some_token",
            ),
        )


async def test_decode_jwt_returns_the_decoded_jwt_payload():
    returned_key = MagicMock(spec=PyJWK)
    returned_key.key = "some_key"
    mock_jwks_client = MagicMock(spec=PyJWKClient)
    mock_jwks_client.get_signing_key_from_jwt = MagicMock(return_value=returned_key)

    with patch("jwt.decode", return_value={"decoded": "token"}):
        result = await decode_jwt(
            security_scopes=SecurityScopes(),
            config=AppConfig(),
            jwks_client=mock_jwks_client,
            token=HTTPAuthorizationCredentials(
                # The token cannot be decrypted and will trigger the exception
                scheme="bearer",
                credentials="some_token",
            ),
        )

    assert result == {"decoded": "token"}
