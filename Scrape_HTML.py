import pandas as pd
from bs4 import BeautifulSoup
import requests
import html2text
import multiprocessing


def html_helper(link):
    """
    Returns all visible text on a webpage
    """
    try:
        page = requests.get(link, timeout=3.05)
    except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout,
            requests.packages.urllib3.exceptions.LocationValueError) as e:
        page = requests.Response()
        page.status_code = 404
    if (not page.history and page.status_code == 200) or \
       (page.history and page.history[0].status_code == 301):
        h = html2text.HTML2Text()
        h.ignore_links = True
        h.ignore_images = True
        h.ignore_emphasis = True
        return h.handle(page.text)
    else:
        return "empty"


def get_paragraph_txt(link):
    """
    Return all paragraph text within the body tag
    """
    try:
        page = requests.get(link, timeout=3.05)
    except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout,
            requests.packages.urllib3.exceptions.LocationValueError) as e:
        page = requests.Response()
        page.status_code = 404
    if (not page.history and page.status_code == 200) or \
       (page.history and page.history[0].status_code == 301):
        soup = BeautifulSoup(page.content, 'html.parser')
        text = [txt.get_text() for txt in soup.select('body p')]
        return ' '.join(text).encode('utf-8')
    else:
        return "empty"


def links_parallel(url_fn, links_lst):
    """
    Return the output of an html helper function
    """
    pool = multiprocessing.Pool(4)
    processed_links = pool.map(url_fn, links_lst)
    return processed_links


def main():
    pass


if __name__ == '__main__':
    # main()
    file_path = 'Data/bookmarks_chrome.html'
    with open(file_path, 'r') as f:
        soup = BeautifulSoup(f, 'html.parser')
    links = [link.get('href') for link in soup.find_all('a') if
             link.get('href').startswith('http') and not
             link.get('href').endswith('.pdf')]
    d = {'links': links}
    df = pd.DataFrame(d)
    processed_links = links_parallel(html_helper, links)
    df['text'] = processed_links
    df.to_pickle('Data/df_website_content.pkl')
