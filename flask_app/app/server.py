import requests

from urllib.parse import urlparse
from flask import request, Response, make_response

from app import app, logger

CHUNK_SIZE = 1024


@app.route('/', methods=["GET", "POST", "PUT", "DELETE"])
@app.route('/<path:path>', methods=["GET", "POST", "PUT", "DELETE"])
def google_page(path='zapretno.info/klip-haski-iuda'):
    if not path.startswith('http'):
        path = 'http://' + path
    logger.info(f'Fetching {path}')
    proxy_ref = proxy_ref_info(request)
    headers = {"Referer": f'http://{proxy_ref[0]}/{proxy_ref[1]}'} if proxy_ref else {}
    logger.info(f'Fetching with headers: {path}, {headers}')
    resp = requests.get(path, stream=True, params=request.args, headers=headers)
    logger.info(f'Got {resp.status_code} response from {path}')
    return Response(
        generate(response=resp),
        # headers=request.headers,
    )


def generate(response):
    for chunk in response.iter_content(CHUNK_SIZE):
        yield chunk


def split_url(url):
    """Splits the given URL into a tuple of (protocol, host, uri)"""
    proto, rest = url.split(':', 1)
    rest = rest.split('/', 1)
    host, uri = (rest[0], rest[1]) if len(rest) == 2 else (rest[0], "")
    return proto, host, uri


def proxy_ref_info(req):
    """Parses out Referer info indicating the request is from a previously proxied page.
    For example, if:
        Referer: http://localhost:8080/p/google.com/search?q=foo
    then the result is:
        ("google.com", "search?q=foo")
    """
    ref = req.host_url + req.full_path[1:]
    if ref:
        _, _, uri = split_url(ref)
        if uri.find("/") < 0:
            return None
        first, rest = uri.split("/", 1)
        # if first in "pd":
        parts = rest.split("/", 1)
        r = (parts[0], parts[1]) if len(parts) == 2 else (parts[0], "")
        logger.info(f'Referred by proxy host, uri: {r[0]}, {r[1]}')
        return r
    return None
