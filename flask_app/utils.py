import re

from urllib.parse import urlparse


def find_all_relative_urls(content):
    """
    Find all urls in the web page
    :param content: html content of the web page
    :return: list of urls
    """
    return [url[1] for url in re.findall(r'(src|href)="(?P<url>/[^"]*)"', content, flags=re.IGNORECASE) if url]


def replace_with_host(urls, host, content):
    """
    Replace all relative urls (from `urls`) in the content into the absolute paths
    :param urls: list of urls in the content to replace
    :param host: domain name of the web site
    :param content: html content of the web page
    :return: new html source
    """
    for url in urls:
        content = content.replace(f'"{url}"', f'{host}{url}')
    return content


def get_host(path):
    parsed = urlparse(path)
    return parsed.netloc, parsed.path


if __name__ == '__main__':
    content = """
    <script src="https://code.jquery.com/jquery-2.2.0.min.js" type="text/javascript"></script>
    <script src="/wp-content/themes/zapretno3/slick/slick/slick.js" type="text/javascript" charset="utf-8"></script>
    <link rel="stylesheet" type="text/css" href="/wp-content/themes/zapretno3/slick/slick/slick.css">
    <link rel="stylesheet" type="text/css" href="/wp-content/themes/zapretno3/slick/slick/slick-theme.css">"""

    result = find_all_relative_urls(content=content)
    print(result)
    result = replace_with_host(urls=result, host='zapretno.info', content=content)
    print(result)

    url1 = 'http://localhost:9000/google.com/about/?search'
    url2 = 'http://google.com/about/?search'
    print(get_host(url1))
    print(get_host(url2))
