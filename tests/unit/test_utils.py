from readwise.cli import check_token


def test_provided_token():
    token = "test_token"
    assert check_token(token) == token
