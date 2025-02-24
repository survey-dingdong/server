from http.client import HTTPConnection
from unittest.mock import AsyncMock, Mock, patch

import pytest
from jwt import PyJWT
from jwt.exceptions import PyJWTError

from app.user.domain.vo import LoginTypeEnum
from core.fastapi.middlewares import authentication
from core.fastapi.middlewares.authentication import AuthBackend, CurrentUser
from tests.support.constants import DEFAULT_USER_ID


@pytest.fixture
def conn_mock() -> Mock:
    return Mock(spec=HTTPConnection)


@pytest.fixture
def redis_backend() -> AsyncMock:
    mock = AsyncMock()
    mock.redis_client.validate_login_session.return_value = True
    return mock


@pytest.fixture
def auth_backend() -> AuthBackend:
    return AuthBackend()


class TestAuthentication:
    @pytest.mark.asyncio
    @patch.object(authentication, "jwt")
    async def test_empty_header(
        self, jwt_mock: PyJWT, conn_mock: Mock, auth_backend: AuthBackend
    ) -> None:
        # Given
        conn_mock.headers = {}
        jwt_mock.decode.return_value = {"user_id": DEFAULT_USER_ID}

        # When
        authenticated, user = await auth_backend.authenticate(conn=conn_mock)

        # Then
        assert authenticated is False
        assert user.id is None
        assert user.login_type is None

    @pytest.mark.asyncio
    @patch.object(authentication, "jwt")
    async def test_invalid_header(
        self, jwt_mock: PyJWT, conn_mock: Mock, auth_backend: AuthBackend
    ) -> None:
        # Given
        conn_mock.headers = {"Authorization": "Bearer1234"}
        jwt_mock.decode.return_value = {"user_id": DEFAULT_USER_ID}

        # When
        authenticated, user = await auth_backend.authenticate(conn=conn_mock)

        # Then
        assert authenticated is False
        assert user.id is None
        assert user.login_type is None

    @pytest.mark.asyncio
    @patch.object(authentication, "jwt")
    async def test_not_startswith_bearer(
        self, jwt_mock: PyJWT, conn_mock: Mock, auth_backend: AuthBackend
    ) -> None:
        # Given
        conn_mock.headers = {"Authorization": "dingdong-survey 1234"}
        jwt_mock.decode.return_value = {"user_id": 1}

        # When
        authenticated, user = await auth_backend.authenticate(conn=conn_mock)

        # Then
        assert authenticated is False
        assert user.id is None
        assert user.login_type is None

    @pytest.mark.asyncio
    @patch.object(authentication, "jwt")
    async def test_empty_credentials(
        self, jwt_mock: PyJWT, conn_mock: Mock, auth_backend: AuthBackend
    ) -> None:
        # Given
        conn_mock.headers = {"Authorization": "Bearer "}
        jwt_mock.decode.return_value = {"user_id": 1}

        # When
        authenticated, user = await auth_backend.authenticate(conn=conn_mock)

        # Then
        assert authenticated is False
        assert user.id is None
        assert user.login_type is None

    @pytest.mark.asyncio
    @patch.object(authentication, "jwt")
    async def test_invalid_token(
        self, jwt_mock: PyJWT, conn_mock: Mock, auth_backend: AuthBackend
    ) -> None:
        # Given
        conn_mock.headers = {"Authorization": "Bearer"}
        jwt_mock.decode.side_effect = PyJWTError

        # When
        authenticated, user = await auth_backend.authenticate(conn=conn_mock)

        # Then
        assert authenticated is False
        assert user.id is None
        assert user.login_type is None

    @pytest.mark.asyncio
    @patch.object(authentication, "jwt")
    async def test_invalid_jwt_token_field(
        self, jwt_mock: PyJWT, conn_mock: Mock, auth_backend: AuthBackend
    ) -> None:
        # Given
        conn_mock.headers = {"Authorization": "bearer credentials"}
        jwt_mock.decode.return_value = {
            "user_id": DEFAULT_USER_ID,
        }

        # When
        authenticated, user = await auth_backend.authenticate(conn=conn_mock)

        # Then
        assert authenticated is False
        assert user == CurrentUser(id=DEFAULT_USER_ID)

    @pytest.mark.asyncio
    @patch.object(authentication, "jwt")
    async def test_valid_authentication(
        self,
        jwt_mock: PyJWT,
        conn_mock: Mock,
        redis_backend: AsyncMock,
        auth_backend: AuthBackend,
    ) -> None:
        # Given
        conn_mock.headers = {"Authorization": "bearer credentials"}
        jwt_mock.decode.return_value = {
            "user_id": DEFAULT_USER_ID,
            "login_type": LoginTypeEnum.Web,
        }

        # When
        authenticated, user = await auth_backend.authenticate(
            conn=conn_mock, redis_client=redis_backend
        )

        # Then
        assert authenticated is True
        assert user == CurrentUser(id=DEFAULT_USER_ID, login_type=LoginTypeEnum.Web)
