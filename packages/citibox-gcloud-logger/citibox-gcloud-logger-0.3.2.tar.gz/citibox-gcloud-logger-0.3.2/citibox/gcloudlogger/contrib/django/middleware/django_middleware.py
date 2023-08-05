import logging
import time
import json

from django.http.request import HttpRequest


class DjangoMiddleware:
    DJANGO_HEADER_PREFIX = "HTTP_"
    PUBSUB_USER_AGENT = "CloudPubSub-Google"

    def __init__(self, get_response):
        self._get_response = get_response
        self.logger = logging.getLogger()

    def __call__(self, request):
        start = self._get_current_timestamp()
        request_details = self._log_request(request)

        response = self._get_response(request)

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

    def _log_request(self, request: HttpRequest):
        method = request.method
        query_details = {
            "host": request.get_host(),
            "path": request.path,
            "request": {
                "method": method,
                "headers": {k[len(self.DJANGO_HEADER_PREFIX):]: v for k, v in request.META.items()} if request.META else {}
            }
        }

        if method in ("GET", "DELETE"):
            query_details["request"].update({"params": {item[0]: item[1] for item in request.GET.lists()}})
        elif method in ("POST", "PUT", "PATCH"):
            query_details["request"].update({"body": request.POST if len(request.POST) > 0 else json.loads(request.body)})
            if request.META.get('HTTP_USER_AGENT') == self.PUBSUB_USER_AGENT:
                try:
                    [query_details.update({k: v for k, v in request.POST.get('message')['attributes'].items()})]
                except KeyError as e:  # pragma: no cover
                    self.logger.warning(f'Cannot load pubsub message attributes')

        return query_details
