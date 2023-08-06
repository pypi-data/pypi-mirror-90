import pytest
import dibuk

from dibuk.error import APIError
from dibuk.resource import Auth


class TestAuth(object):
    def test_invalid_auth_instantiation_with_no_credentials(self):
        with pytest.raises(APIError):
            dibuk.api_credentials = None
            Auth()

    def test_invalid_auth_instantiation_with_empty_credentials(self):
        with pytest.raises(APIError):
            dibuk.api_credentials = ()
            Auth()

    def test_invalid_auth_instantiation_with_incomplete_credentials(self):
        with pytest.raises(APIError):
            dibuk.api_credentials = ("client_id",)
            Auth()

    def test_signing_data_with_unicode_strings(self):
        dibuk.api_credentials = (
            "client_id",
            "client_secret",
        )
        auth = Auth()
        signature = auth.sign([("name", u"Gundar-Gošen Ajelet")])
        assert signature == "dea946d5dcc7ea93aedcf4709ecc680e7249c2aa"
