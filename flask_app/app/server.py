import requests

from flask import request, Response


from utils import replace_with_host, find_all_relative_urls, get_host
from app import app, logger

CHUNK_SIZE = 1024


@app.route('/', methods=["GET", "POST", "PUT", "DELETE"])
@app.route('/<path:path>', methods=["GET", "POST", "PUT", "DELETE"])
def google_page(path='zapretno.info/klip-haski-iuda'):
    logger.info(f'Fetching {path}')
    if 'localhost' in request.host_url:
        if not path.startswith('http'):
            path = 'http://' + path
        domain, suffix = get_host(path)
        domain = f'http://{domain}'
    else:
        domain, suffix = request.host_url, path
    resp = requests.get(f'{domain}{suffix}', stream=True, params=request.args, timeout=5)
    all_urls = find_all_relative_urls(resp.content.decode('utf-8', errors='ignore'))
    logger.info('Urls in the web page: ' + str(all_urls))

    if all_urls:
        new_content = replace_with_host(urls=all_urls, host=domain, content=resp.content.decode(encoding='utf-8'))
        logger.info('Get new content')
        resp._content = new_content.encode('utf-8')

    logger.info(f'Got {resp.status_code} response from {path}')
    return Response(
        generate(response=resp),
    )


def generate(response):
    for chunk in response.iter_content(CHUNK_SIZE):
        yield chunk
