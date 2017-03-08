import pandas as pd
from bs4 import BeautifulSoup
import requests
import html2text
import multiprocessing


def get_url_content(link):
    """
    Return text visible on html page.
    Note: could have used unidecode(soup.text)
    """
    r = requests.get(link, allow_redirects=False)
    if r.status_code == 200:
        return h.handler(r.text)
    else:
        return "broken_link"


def main():
    pass


if __name__ == '__main__':
    # main()
    h = html2text.HTML2Text()
    h.ignore_links = True
    h.ignore_images = True
    h.ignore_emphasis = True
    file_path = '../Data/bookmarks.html'
    with open(file_path, 'r') as f:
        soup = BeautifulSoup(f, 'html.parser')
    links = [link.get('href') for link in soup.find_all('a') if
             link.get('href').startswith('http')]
    d = {'links': links}
    df = pd.DataFrame(d)
    pool = multiprocessing.Pool(3)
    processed_links = pool.map(get_url_content, links)
    # df['content'] = df['links'].apply(get_url_content)
