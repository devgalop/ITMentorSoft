from src.features.user_management.change_password.change_password_request import (
    ChangePasswordRequest,
    ChangePasswordRequestWithToken,
)
import pytest


def test_when_token_is_valid_and_new_password_is_provided_then_no_validation_errors():
    new_pass = "NewSecPass123!"
    request = ChangePasswordRequest(new_password=new_pass)
    token = "valid_token"
    id_trx = "valid_id_trx"
    change_password_request = ChangePasswordRequestWithToken(
        token=token, id_trx=id_trx, new_password=request.new_password
    )
    assert change_password_request.token == token
    assert change_password_request.id_trx == id_trx
    assert change_password_request.new_password == new_pass


def test_when_token_is_missing_then_validation_error():
    new_pass = "NewSecPass123!"
    request = ChangePasswordRequest(new_password=new_pass)
    token = ""
    id_trx = "valid_id_trx"
    with pytest.raises(ValueError, match="Token is required"):
        ChangePasswordRequestWithToken(
            token=token, id_trx=id_trx, new_password=request.new_password
        )


def test_when_id_trx_is_missing_then_validation_error():
    new_pass = "NewSecPass123!"
    request = ChangePasswordRequest(new_password=new_pass)
    token = "valid_token"
    id_trx = ""
    with pytest.raises(ValueError, match="Transaction ID is required"):
        ChangePasswordRequestWithToken(
            token=token, id_trx=id_trx, new_password=request.new_password
        )


def test_when_new_password_is_missing_then_validation_error():
    with pytest.raises(ValueError, match="Password is required"):
        ChangePasswordRequest(new_password="")


def test_when_new_password_is_too_short_then_validation_error():
    new_pass = "Ab1!"
    with pytest.raises(ValueError, match="Password must be at least 6 characters long"):
        ChangePasswordRequest(new_password=new_pass)


def test_when_new_password_is_too_long_then_validation_error():
    new_pass = "A" * 21 + "1!"
    with pytest.raises(
        ValueError, match="Password must be no more than 20 characters long"
    ):
        ChangePasswordRequest(new_password=new_pass)


def test_when_new_password_has_no_digit_then_validation_error():
    new_pass = "NewSecPass!"
    with pytest.raises(ValueError, match="Password must contain at least one digit"):
        ChangePasswordRequest(new_password=new_pass)


def test_when_new_password_has_no_letter_then_validation_error():
    new_pass = "12345678!"
    with pytest.raises(ValueError, match="Password must contain at least one letter"):
        ChangePasswordRequest(new_password=new_pass)


def test_when_new_password_has_no_special_char_then_validation_error():
    new_pass = "NewSecPass123"
    with pytest.raises(
        ValueError, match="Password must contain at least one special character"
    ):
        ChangePasswordRequest(new_password=new_pass)
