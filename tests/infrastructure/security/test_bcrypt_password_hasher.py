from src.infrastructure.security.bcrypt_password_hasher import BcryptPasswordHasher


def test_when_hash_password_called_then_returns_string_different_from_plain_text():
    hasher = BcryptPasswordHasher()
    plain = "mypassword123!"
    result = hasher.hash_password(plain)
    assert result != plain


def test_when_hash_password_called_then_returns_valid_bcrypt_hash():
    hasher = BcryptPasswordHasher()
    result = hasher.hash_password("mypassword123!")
    assert result.startswith("$2b$")


def test_when_verify_password_called_with_correct_password_then_returns_true():
    sample_pass = "secret123!"
    hasher = BcryptPasswordHasher()
    hashed = hasher.hash_password(sample_pass)
    assert hasher.verify_password(sample_pass, hashed) is True


def test_when_verify_password_called_with_wrong_password_then_returns_false():
    hasher = BcryptPasswordHasher()
    hashed = hasher.hash_password("correct_pass1!")
    assert hasher.verify_password("wrong_pass1!", hashed) is False


def test_when_hash_password_called_twice_then_produces_different_hashes():
    hasher = BcryptPasswordHasher()
    password = "same_password_123!"
    hash1 = hasher.hash_password(password)
    hash2 = hasher.hash_password(password)
    assert hash1 != hash2
