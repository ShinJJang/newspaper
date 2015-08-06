from bs4 import BeautifulSoup
import urllib.request


def get_content(url):
    req = urllib.request.Request(url, headers={'User-Agent': "Magic Browser"})
    response = urllib.request.urlopen(req).read()
    return response


def parse_title(url):
    soup = BeautifulSoup(get_content(url), "html.parser")
    title = soup.title.string
    if not title:
        title = soup.find("meta", property="og:title")['content']  # The open graph protocol http://ogp.me/
    return title