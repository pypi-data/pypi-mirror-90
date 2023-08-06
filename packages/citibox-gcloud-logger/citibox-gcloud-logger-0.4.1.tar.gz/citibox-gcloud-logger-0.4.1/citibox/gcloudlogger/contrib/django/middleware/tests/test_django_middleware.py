from unittest import mock
import json

from citibox.gcloudlogger.contrib.django import DjangoMiddleware
from citibox.gcloudlogger.src.gcloud_formatter import GCloudFormatter
from citibox.gcloudlogger.test_helpers.logger_test_case import LoggerTestCase


class EmptyResource:
    pass


class FakeResponse:
    content = json.dumps({"some_key": "some_value"})
    data = '{"some_key": "some_value"}'
    status_code = "200 Ok"


@mock.patch('citibox.gcloudlogger.contrib.django.middleware.django_middleware.HttpRequest')
class TestDjangoMiddleware(LoggerTestCase):
    logger = None
    _formatter = GCloudFormatter
    logger_name = __name__

    def test_process_request_get_http(self, request_mock):
        django_middleware = DjangoMiddleware(lambda x: FakeResponse())
        request_mock.get_host.return_value = "fake_host.com"
        request_mock.path = "/fake/path"
        request_mock.method = "GET"
        request_mock.META = {
            "HTTP_HEADER_1": "header_1"
        }
        request_mock.GET.lists.return_value = [
            ("param", "value")
        ]

        result = django_middleware(request_mock)
        last_log = json.loads(self.memory_logger.last_record)

        self.assertIsInstance(result, FakeResponse)
        self.assertEquals(f'{request_mock.method} 200 Ok {request_mock.path}', last_log.get('message'))
        self.assertIn("headers", last_log.get('request'))
        self.assertIn("host", last_log)
        self.assertIn("path", last_log)
        self.assertEquals("value", last_log.get('request').get("params").get("param"))
        self.assertEquals("header_1", last_log.get('request').get("headers").get("HEADER_1"))
        self.assertEquals(json.loads(FakeResponse.content), last_log.get("response").get("body"))

    def test_process_request_post_http(self, request_mock):
        django_middleware = DjangoMiddleware(lambda x: FakeResponse())
        request_mock.get_host.return_value = "fake_host.com"
        request_mock.path = "/fake/path"
        request_mock.method = "POST"
        request_mock.META = {
            "HTTP_HEADER_1": "header_1"
        }
        request_mock.POST = {
            "param": "value"
        }

        result = django_middleware(request_mock)
        last_log = json.loads(self.memory_logger.last_record)

        self.assertIsInstance(result, FakeResponse)
        self.assertEquals(f'{request_mock.method} 200 Ok {request_mock.path}', last_log.get('message'))
        self.assertIn("headers", last_log.get('request'))
        self.assertIn("host", last_log)
        self.assertIn("path", last_log)
        self.assertEquals("value", last_log.get('request').get("body").get("param"))
        self.assertEquals("header_1", last_log.get('request').get("headers").get("HEADER_1"))
        self.assertEquals(json.loads(FakeResponse.content), last_log.get("response").get("body"))

    def test_process_request_post_pubsub_http(self, request_mock):
        django_middleware = DjangoMiddleware(lambda x: FakeResponse())
        request_mock.get_host.return_value = "fake_host.com"
        request_mock.path = "/fake/path"
        request_mock.method = "POST"
        request_mock.META = {
            "HTTP_HEADER_1": "header_1",
            "HTTP_USER_AGENT": DjangoMiddleware.PUBSUB_USER_AGENT
        }
        request_mock.POST = {
            "message": {
                "attributes": {"attr_1": "AA"}
            }
        }

        result = django_middleware(request_mock)
        last_log = json.loads(self.memory_logger.last_record)

        self.assertIsInstance(result, FakeResponse)
        self.assertEquals(f'{request_mock.method} 200 Ok {request_mock.path}', last_log.get('message'))
        self.assertIn("headers", last_log.get('request'))
        self.assertIn("host", last_log)
        self.assertIn("path", last_log)
        self.assertEquals("AA", last_log.get("attr_1"))
        self.assertEquals("header_1", last_log.get('request').get("headers").get("HEADER_1"))
        self.assertEquals(json.loads(FakeResponse.content), last_log.get("response").get("body"))

    def test_process_request_post_pubsub_http_without_attributes(self, request_mock):
        django_middleware = DjangoMiddleware(lambda x: FakeResponse())
        request_mock.get_host.return_value = "fake_host.com"
        request_mock.path = "/fake/path"
        request_mock.method = "POST"
        request_mock.META = {
            "HTTP_HEADER_1": "header_1",
            "HTTP_USER_AGENT": DjangoMiddleware.PUBSUB_USER_AGENT
        }
        request_mock.POST = {
            "message": {
                "attributes": {}
            }
        }

        result = django_middleware(request_mock)
        last_log = json.loads(self.memory_logger.last_record)

        self.assertIsInstance(result, FakeResponse)
        self.assertEquals(f'{request_mock.method} 200 Ok {request_mock.path}', last_log.get('message'))
        self.assertIn("headers", last_log.get('request'))
        self.assertIn("host", last_log)
        self.assertIn("path", last_log)
        self.assertEquals("header_1", last_log.get('request').get("headers").get("HEADER_1"))
        self.assertNotIn("attr_1", last_log)
        self.assertEquals(json.loads(FakeResponse.content), last_log.get("response").get("body"))