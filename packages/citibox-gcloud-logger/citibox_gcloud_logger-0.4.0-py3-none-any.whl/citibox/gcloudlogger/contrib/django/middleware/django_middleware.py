import json
import re

from django.http.request import HttpRequest

from citibox.gcloudlogger.contrib import Middleware

BINARY_REGEX = re.compile(r"(.+(Content-Type):.*?)(\S+)/(\S+)(?:\r\n)*(.+)", re.S | re.I | re.IGNORECASE)
BINARY_TYPES = ("image", "application")


class DjangoMiddleware(Middleware):
    DJANGO_HEADER_PREFIX = "HTTP_"
    PUBSUB_USER_AGENT = "CloudPubSub-Google"

    def __init__(self, get_response):
        super().__init__()
        self._get_response = get_response
        self._cached_request_body = None
        self._url_fingerprint = ""

    def __call__(self, request):
        start = self._get_current_timestamp()
        self._cached_request_body = request.body
        response = self._get_response(request)
        request_details = self._log_request(request)

        try:
            body = None
            if hasattr(response, 'data') and response.data:
                body = json.loads(response.content)
            request_details['response'] = {
                'body': body
            }
        except json.JSONDecodeError as e:
            request_details["response"] = {
                "body": f'Error serializing response: {e.msg}'
            }

        request_details.update({"duration": (self._get_current_timestamp() - start) / 1000})
        request_details.update({
            "url_fingerprint": self._url_fingerprint
        })

        try:
            self.logger.info(
                f'{request.method} {response.status_code} {request.path}',
                extra=request_details
            )
        except Exception:  # pragma: no cover
            pass

        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        self._url_fingerprint = self._get_url_fingerprint(request.path, view_kwargs)

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
                    pubsub_attributes = request.POST.get('message')['attributes']
                    if len(pubsub_attributes) > 0:
                        query_details.update(pubsub_attributes.items())
                except Exception as e:  # pragma: no cover
                    self.logger.warning(f'Cannot load pubsub message attributes on logger middleware: {e}')

        return query_details
