import pytest
from datetime import timedelta
from app.core import (
    get_password_hash,
    verify_password,
    create_access_token,
    decode_access_token,
)


def test_password_hash_and_verify():

    password = "secret321"
    hashed = get_password_hash(password)

    assert hashed != password
    assert hashed.startswith("$2b$") or hashed.startswith("$2a$")

    assert verify_password(password, hashed)
    assert not verify_password("wrong-password", hashed)


def test_create_access_token_default_exp():

    data = {"sub": "testuser"}
    token = create_access_token(data)

    assert isinstance(token, str)
    decoded = decode_access_token(token)

    assert decoded.get("sub") == "testuser"
    assert "exp" in decoded


def test_create_access_token_with_custom_exp():

    data = {"sub": "customuser"}
    token = create_access_token(data, expires_delta=timedelta(minutes=60))
    decoded = decode_access_token(token)

    assert decoded.get("sub") == "customuser"
    assert decoded["exp"] is not None


def test_decode_access_token_invalid_token():

    invalid = "this.is.not.valid"
    decoded = decode_access_token(invalid)

    assert decoded == {}

    token = create_access_token({"sub": "hacker"})
    tampered = token + "123"
    decoded = decode_access_token(tampered)

    assert decoded == {}
