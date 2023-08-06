from falcon import Request, Response

from citibox.gcloudlogger.contrib import Middleware


class FalconMiddleware(Middleware):
    PUBSUB_USER_AGENT = "CloudPubSub-Google"

    def _get_request_details(self, req: Request):
        method = req.method
        query_details = {
            "host": req.host,
            "path": req.path,
            "request": {
                "method": method,
                "headers": req.headers
            }
        }

        if method in ("GET", "DELETE"):
            query_details["request"].update({"params": req.params})
        elif method in ("POST", "PUT", "PATCH"):
            query_details["request"].update({"body": req.media})
            if req.user_agent == self.PUBSUB_USER_AGENT:
                try:
                    [query_details.update({k: v}) for k, v in req.media['message']['attributes'].items()]
                except KeyError as e:  # pragma nocover
                    self.logger.warning(f'Cannot load pubsub message attributes')

        return query_details

    def process_request(self, req: Request, resp: Response):
        """

        :param req: falcon.Request
        :param resp: falcon.Response
        :return:
        """
        req.context.started_at = self._get_current_timestamp()

    def process_resource(self, req: Request, resp: Response, resource, params: dict):
        req.context.url_fingerprint = self._get_url_fingerprint(
            req.path,
            params
        )

    def process_response(self, req: Request, resp: Response, resource, req_succeeded: bool):
        """

        :param req: falcon.Request
        :param resp: falcon.Response
        :param resource: Resource object
        :param req_succeeded: bool
        :return:
        """
        response_detail = self._get_request_details(req)
        if hasattr(req.context, "url_fingerprint"):
            response_detail.update({'url_fingerprint': req.context.url_fingerprint})
        response_detail["response"] = {
            "body": resp.body,
            "http_status": resp.status,
            "headers": resp.headers
        }
        response_detail.update({"duration": (self._get_current_timestamp() - req.context.started_at) / 1000})
        try:
            self.logger.info(
                f'{req.method} {resp.status} {req.path}',
                extra=response_detail
            )
        except Exception as e:  # pragma nocover
            pass
