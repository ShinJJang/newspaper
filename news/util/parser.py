from bs4 import BeautifulSoup
import urllib.request


def get_content(url):
    """This function is intended to return content from url.

    :param url: URL to get content
    :return: The response from url
    """
    req = urllib.request.Request(url, headers={'User-Agent': "Magic Browser"})
    response = urllib.request.urlopen(req).read()
    return response


def parse_title(url):
    """This function is intended to parse title from url and return it.

    :param url: URL to get title
    :return: The title of url
    """
    soup = BeautifulSoup(get_content(url), "html.parser")
    title = soup.title.string
    if not title:
        title = soup.find("meta", property="og:title")['content']  # The open graph protocol http://ogp.me/
    return title