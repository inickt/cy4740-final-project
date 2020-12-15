from typing import Optional

from mitmproxy import ctx, http

class CaptureAddon:
    def __init__(self):
        self.label: Optional[str] = None

    # TODO use the current label to save information from the request and responses
    def request(self, flow: http.HTTPFlow) -> None:
        print(flow)

    def response(self, flow: http.HTTPFlow) -> None:
        print(flow)
