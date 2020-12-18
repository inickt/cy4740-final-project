from collections import defaultdict, namedtuple
from dataclasses import dataclass
from typing import Optional

from mitmproxy import ctx, http

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
                    "issuer": {
                        issuer_type.decode("utf8"): issuer_contents.decode("utf8")
                        for issuer_type, issuer_contents in flow.server_conn.cert.issuer
                    }
                    if flow.server_conn.cert.issuer
                    else None,
                    "notbefore": flow.server_conn.cert.notbefore.isoformat(),
                    "notafter": flow.server_conn.cert.notafter.isoformat(),
                    "has_expired": flow.server_conn.cert.has_expired,
                    "subject": {
                        subject_type.decode("utf8"): subject_contents.decode("utf8")
                        for subject_type, subject_contents in flow.server_conn.cert.subject
                    }
                    if flow.server_conn.cert.subject
                    else None,
                    "serial": flow.server_conn.cert.serial,
                    "cn": flow.server_conn.cert.cn.decode("utf8")
                    if flow.server_conn.cert.cn
                    else None,
                    "organization": flow.server_conn.cert.organization.decode("utf8")
                    if flow.server_conn.cert.organization
                    else None,
                    "altnames": [
                        name.decode("utf8") for name in flow.server_conn.cert.altnames
                    ]
                    if flow.server_conn.cert.altnames
                    else None,
                }
                if flow.server_conn.cert
                else None,
                flow.server_conn.sni,
                flow.server_conn.tls_version,
            )
            self.captures[self.label].append(request._asdict())

    def response(self, flow: http.HTTPFlow) -> None:
        # we could do something with responses here if we want, but for the focus of this project
        # we only ended up looking at outgoing requests
        pass
