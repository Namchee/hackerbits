import grequests
import requests
from urllib.robotparser import RobotFileParser
from typing import List, Tuple
from datetime import datetime
from os import getcwd
from bs4 import BeautifulSoup
from math import ceil
from random import randint
from time import sleep
from json import dump
from newspaper.article import ArticleException
from newspaper import Article, Config, news_pool

from src.model.news import News

class CrawlingResult:
    def __init__(self, news: List[News], time: datetime) -> None:
        self.news = news
        self.time = time

    def write_result_to_file(self, dir = getcwd(), name = 'crawling_result') -> None:
        """Write crawling result to a JSON file
        Args:
            dir (str, optional): Directory to be written. Defaults to getcwd().
            name (str, optional): File name. Defaults to 'crawling_result'.
        """
        with open(f'{dir}/{name}.json', 'w') as file:
            data = {
                'fetched_at': self.time.isoformat(),
                'news': list(map(lambda o: o.__dict__, self.news)),
            }

            dump(data, file, indent=4, ensure_ascii=True)

def _parse_response_body(resp_body: str) -> List[str]:
    """Extract news URLs from HackerNews body page

    Args:
        resp_body (str): [description]

    Returns:
        List[str]: [description]
    """
    base_url = "https://news.ycombinator.com"
    urls = []

    body_parser = BeautifulSoup(resp_body, 'html.parser')
    titles = body_parser.select('.storylink')

    for news_title in titles:
        url = news_title.get('href')

        if not url.startswith('http'):
            url = f'{base_url}/{url}'
            
        if not url.endswith('.pdf'):
            urls.append(url)

    return urls

def _get_news_metadata(urls: List[str]) -> List[News]:
    """Get news' metadata from URL

    Args:
        urls (List[str]): List of news URL

    Returns:
        List[News]: List of parsed article contents
    """
    config = Config()
    config.browser_user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
    config.fetch_images = False # DO NOT fetch the image

    news_list = list(map(lambda url: Article(url=url, config=config), urls))
    news_pool.set(news_list)
    news_pool.join()

    result = []

    for news in news_list:
        try:
            news.parse()

            result.append(
                News(
                    authors=news.authors,
                    title=news.title,
                    published_at=news.publish_date,
                    contents=news.text
                )
            )
        except ArticleException: # Ignore non articles
            pass

    return result

def _fetch_news_sync(limit: int, page: int = 1) -> Tuple[List[str], int]:
    """Crawl HackerNews website for fresh tech article links SYNCHRONOUSLY

    Args:
        limit (int): Limits how much articles should be fetched.
        page (int, optional): Determine the starting page.

    Returns:
        Tuple(List[str], int): List of URLs and next page number to be fetched
    """
    base_url = "https://news.ycombinator.com"
    delay = 0
    pages = ceil(limit / 30)

    rp = RobotFileParser(url=f'{base_url}/robots.txt')
    rp.read()
    crawl_delay = rp.crawl_delay('*')

    if crawl_delay is not None:
        delay = int(crawl_delay)

    resp_body = []
    count = 0

    while count < pages:
        resp = requests.get(f'{base_url}/news?p={page}')
            
        resp_body.append(resp.text)
        count += 1
        page += 1

        if pages - count > 1:
            sleep(randint(delay, delay + 10)) # Simulate 'humans' access time

    urls = []

    for body in resp_body:
        urls.extend(_parse_response_body(body))

    return (urls, page)

def _fetch_news_async(limit: int, page: int = 1) -> Tuple[List[str], int]:
    """Crawl HackerNews website for fresh tech article links with paralel
    requests. Faster, but not polite at all

    Args:
        limit (int): Limits how much articles should be fetched.
        page (int, optional): Determine the starting page.

    Returns:
        Tuple(List[str], int): List of URLs and next page number to be fetched
    """
    base_url = "https://news.ycombinator.com"
    pages = ceil(limit / 30)

    resp_body = []
    reqs = []
    count = 0

    while count < pages:
        reqs.append(f'{base_url}/news?p={page}')
        count += 1
        page += 1

    req = (grequests.get(url) for url in reqs)
        
    for resp in grequests.imap(req):
        resp_body.append(resp.text)

    urls = []

    for body in resp_body:
        urls.extend(_parse_response_body(body))

    return (urls, page)

def crawl_hn_for_news(limit = 200, polite = True) -> CrawlingResult:
    """Crawl HackerNews website for fresh tech articles

    Args:
        limit (int, optional): Limits how much articles should be fetched. Defaults to 200.
        polite (bool, optional): Determine if crawling should be done politely according to robots.txt. Defaults to True.

    Returns:
        CrawlingResult: Crawler results, with timestamp
    """

    urls = None

    if polite:
        urls = _fetch_news_sync(limit)
    else:
        urls = _fetch_news_async(limit)

    news = _get_news_metadata(urls[0])

    if len(news) < limit:
        last_page = _fetch_news_sync(30, urls[1])
        news.extend(_get_news_metadata(last_page[0]))

    return CrawlingResult(
        news=news[0:limit],
        time=datetime.now(),
    )