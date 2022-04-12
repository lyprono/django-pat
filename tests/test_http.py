from django.test import RequestFactory
from django.test import SimpleTestCase
from django.test.utils import override_settings

from django_user_api_key.http import ParseException
from django_user_api_key.http import parse_header


class TestHeaderParsing(SimpleTestCase):
    def setUp(self):
        self.request_factory = RequestFactory()

    def test_it_returns_the_key_value(self):
        req = self.request_factory.get("path", HTTP_AUTHORIZATION="Api-Key 1234")
        parsed_value = parse_header(req)
        self.assertEqual("1234", parsed_value)

    def test_it_returns_null_on_header_not_found(self):
        req = self.request_factory.get("path")
        parsed_value = parse_header(req)
        self.assertIsNone(parsed_value)

    def test_it_returns_error_on_empty_header_value(self):
        req = self.request_factory.get("path", HTTP_AUTHORIZATION="")
        self.assertRaises(ParseException, parse_header, req)

    def test_it_returns_error_on_incorrect_prefix(self):
        req = self.request_factory.get("path", HTTP_AUTHORIZATION="Wrong 1234")
        self.assertRaises(ParseException, parse_header, req)

    @override_settings(USER_API_KEY_CUSTOM_HEADER="X-Custom-Header")
    def test_it_uses_custom_header(self):
        req = self.request_factory.get("path", HTTP_X_CUSTOM_HEADER="Api-Key 1234")
        parsed_value = parse_header(req)
        self.assertEqual("1234", parsed_value)

    @override_settings(USER_API_KEY_CUSTOM_HEADER_PREFIX="Custom-Key")
    def test_it_uses_custom_prefix(self):
        req = self.request_factory.get("path", HTTP_AUTHORIZATION="Custom-Key 1234")
        parsed_value = parse_header(req)
        self.assertEqual("1234", parsed_value)