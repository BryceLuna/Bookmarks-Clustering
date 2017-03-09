import pandas as pd
from bs4 import BeautifulSoup
import requests
import html2text
import multiprocessing
import unidecode
from timeit import Timer


def html_helper(link):
    """
    Helper function to return html text
    Note: consider using unidecode(soup.text)
    """
    h = html2text.HTML2Text()
    h.ignore_links = True
    h.ignore_images = True
    h.ignore_emphasis = True
    r = requests.get(link, allow_redirects=False)
    if r.status_code == 200:
        return h.handle(r.text)
    else:
        return "empty"


def unidecode_helper(link):
    """
    Helper function to return html text
    """
    r = requests.get(link, allow_redirects=False)
    soup = BeautifulSoup(r.text)
    if r.status_code == 200:
        return unidecode(soup.text)
    else:
        return "empty"


def links_parallel(url_fn, links_lst):
    """
    Return text visible on html page.
    """
    pool = multiprocessing.Pool(4)
    processed_links = pool.map(url_fn, links_lst)
    return processed_links


def main():
    pass


if __name__ == '__main__':
    # main()
    file_path = 'Data/bookmarks.html'
    with open(file_path, 'r') as f:
        soup = BeautifulSoup(f, 'html.parser')
    links = [link.get('href') for link in soup.find_all('a') if
             link.get('href').startswith('http') and not
             link.get('href').endswith('.pdf')]
    d = {'links': links}
    df = pd.DataFrame(d)
    # processed_links = links_parallel(html_helper, links)
    t1 = Timer(lambda: links_parallel(html_helper, links))
    t2 = Timer(lambda: links_parallel(unidecode_helper, links))
    print "it took {0} for html2 helper to finish".format(t1.timeit(1))
    print "it took {0} for unidecode to finish".format(t2.timeit(1))
    # df['text'] = processed_links
