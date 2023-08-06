import logging
import time
import json
import re

from django.http.request import HttpRequest

BINARY_REGEX = re.compile(r"(.+(Content-Type):.*?)(\S+)/(\S+)(?:\r\n)*(.+)", re.S | re.I | re.IGNORECASE)
BINARY_TYPES = ("image", "application")


class DjangoMiddleware:
    DJANGO_HEADER_PREFIX = "HTTP_"
    PUBSUB_USER_AGENT = "CloudPubSub-Google"

    def __init__(self, get_response):
        self._get_response = get_response
        self.logger = logging.getLogger()
        self._cached_request_body = None

    def __call__(self, request):
        start = self._get_current_timestamp()
        self._cached_request_body = request.body
        response = self._get_response(request)
        request_details = self._log_request(request)

        request_details["response"] = {
            "body": json.loads(response.content) if hasattr(response, 'data') and response.data else None
        }

        request_details.update({"duration": (self._get_current_timestamp() - start) / 1000})

        try:
            self.logger.info(
                f'{request.method} {response.status_code} {request.path}',
                extra=request_details
            )
        except Exception:  # pragma: no cover
            pass

        return response

    @staticmethod
    def _get_current_timestamp():
        return int(round(time.time() * 1000))

    def _parse_multipart(self, request: HttpRequest, content_type):
        boundary = "--" + content_type[30:]
        try:
            body = self._cached_request_body.decode()
        except UnicodeDecodeError:
            return f'(multipart/form) cannot parse form data'

        parameters = []

        parts = body.split(boundary)
        for index, part in enumerate(parts):
            match = BINARY_REGEX.search(part)
            if match and match.group(2) in BINARY_TYPES and not match.group(4) in ("", "\r\n"):
                part = match.expand(r"\1\2/\3\r\n\r\n(binary data)\r\n")
            parameters.append(part)

        return parameters

    def _log_request(self, request: HttpRequest):
        method = request.method
        query_details = {
            "host": request.get_host(),
            "path": request.path,
            "request": {
                "method": method,
                "headers": {k[len(self.DJANGO_HEADER_PREFIX):]: v for k, v in
                            request.META.items()} if request.META else {}
            }
        }

        if method in ("GET", "DELETE"):
            query_details["request"].update({"params": {item[0]: item[1] for item in request.GET.lists()}})
        elif method in ("POST", "PUT", "PATCH"):
            request_body = ""
            content_type = request.META.get("CONTENT_TYPE", "")
            if content_type.startswith("multipart/form-data"):  # is form-data, we need to parse it
                request_body = self._parse_multipart(request, content_type)
            else:
                try:
                    request_body = request.POST if len(request.POST) > 0 else (
                        json.loads(request.body) if len(request.body) > 0 else {})
                except Exception as e:
                    request_body = "Error when parsing request on logger middleware"

            query_details["request"].update({"body": request_body})
            if request.META.get('HTTP_USER_AGENT') == self.PUBSUB_USER_AGENT:
                try:
                    [query_details.update({k: v for k, v in request.POST.get('message')['attributes'].items()})]
                except KeyError as e:  # pragma: no cover
                    self.logger.warning(f'Cannot load pubsub message attributes')

        return query_details
