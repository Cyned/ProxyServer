from requests import get

from app import app

SITE_NAME = 'https://google.com/'


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def proxy(path):
    return get(f'{SITE_NAME}{path}').content
