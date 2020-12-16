from typing import Optional

from mitmproxy import ctx, http
from dataclasses import dataclass
from collections import defaultdict, namedtuple

from pprint import pprint

from typing import NamedTuple

Request = namedtuple(
    "Request",
    [
        "http_version",
        "timestamp_start",
        "host",
        "port",
        "method",
        "scheme",
        "path",
        "ip_address",
        "tls_established",
        "cert",
        "sni",
        "tls_version",
    ],
)


class CaptureAddon:
    def __init__(self):
        self.label: Optional[str] = None
        self.captures = defaultdict(list)

    def request(self, flow: http.HTTPFlow) -> None:
        if self.label is not None:
            request = Request(
                flow.request.http_version,
                flow.request.timestamp_start,
                flow.request.host,
                flow.request.port,
                flow.request.method,
                flow.request.scheme,
                flow.request.path,
                flow.server_conn.ip_address,
                flow.server_conn.tls_established,
                {
                    # TODO properly serialize if we want these
                    # "issuer": flow.server_conn.cert.issuer,
                    # "notbefore": flow.server_conn.cert.notbefore,
                    # "notafter": flow.server_conn.cert.notafter,
                    # "has_expired": flow.server_conn.cert.has_expired,
                    # "subject": flow.server_conn.cert.subject,
                    "serial": flow.server_conn.cert.serial,
                    "cn": flow.server_conn.cert.cn.decode('ascii'),
                    # "organization": flow.server_conn.cert.organization.decode('ascii'),
                    # "altnames": flow.server_conn.cert.altnames,
                },
                flow.server_conn.sni,
                flow.server_conn.tls_version,
            )
            self.captures[self.label].append(request._asdict())

    def response(self, flow: http.HTTPFlow) -> None:
        # print(flow)
        pass
