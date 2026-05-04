import os
from contextlib import contextmanager

import jwt
from datetime import datetime, timezone, timedelta

from src.infrastructure.security.jwt_token_generator import JWTTokenGenerator
from src.features.user_management.shared.token_generator import (
    InvalidTokenError,
    TokenRequest,
)

os.environ["JWT_SECRET_KEY"] = "test_secret_key_for_testing_purposes_only"
os.environ["JWT_ALGORITHM"] = "HS256"
os.environ["JWT_EXPIRATION_DELTA_SECONDS"] = "300"
os.environ["RANDOM_TOKEN_EXPIRATION_DELTA_SECONDS"] = "180"


@contextmanager
def assert_raises_invalid_token_error():
    try:
        yield
    except InvalidTokenError:
        return
    raise AssertionError("Expected InvalidTokenError to be raised")


def _make_generator() -> JWTTokenGenerator:
    return JWTTokenGenerator()


def _make_request() -> TokenRequest:
    return TokenRequest(user_name="alice", role="student")


def test_when_generate_token_called_then_returns_non_empty_token():
    generator = _make_generator()
    response = generator.generate_token(_make_request())
    assert response.token
    assert len(response.token) > 0


def test_when_generate_token_called_then_returns_future_expiration_time():
    generator = _make_generator()
    response = generator.generate_token(_make_request())
    now = datetime.now(tz=timezone.utc).timestamp()
    assert response.expiration_time > now


def test_when_validate_token_called_with_valid_token_then_returns_correct_user_data():
    generator = _make_generator()
    request = TokenRequest(user_name="alice", role="admin")
    response = generator.generate_token(request)
    data = generator.validate_token(response.token)
    assert data.user_name == "alice"
    assert data.role == "admin"


def test_when_validate_token_called_with_malformed_token_then_raises_invalid_token_error():
    generator = _make_generator()
    with assert_raises_invalid_token_error():
        generator.validate_token("this.is.invalid")


def test_when_validate_token_called_with_wrong_secret_then_raises_invalid_token_error():
    generator = _make_generator()
    wrong_token = jwt.encode(
        {
            "user_name": "alice",
            "role": "admin",
            "exp": datetime.now(tz=timezone.utc) + timedelta(seconds=300),
        },
        "wrong_secret",
        algorithm="HS256",
    )
    with assert_raises_invalid_token_error():
        generator.validate_token(wrong_token)


def test_when_generate_random_token_called_then_returns_non_empty_hex_string():
    generator = _make_generator()
    response = generator.generate_random_token()
    assert response.token
    assert len(response.token) > 0
    assert all(c in "0123456789abcdef" for c in response.token)


def test_when_generate_random_token_called_then_returns_future_expiration():
    generator = _make_generator()
    response = generator.generate_random_token()
    now = datetime.now(tz=timezone.utc).timestamp()
    assert response.expiration_time > now
