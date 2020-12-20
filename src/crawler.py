from urllib.robotparser import RobotFileParser
from typing import List
from datetime import datetime
from os import getcwd
from bs4 import BeautifulSoup
from math import ceil
from random import randint
from time import sleep
from json import dump
from newspaper.article import ArticleException
from newspaper import Article, Config, news_pool
import grequests
import requests

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
                'news': list(map(lambda article: article.toJson(), self.news))
            }

            dump(data, file, indent=4, ensure_ascii=True)

def _get_news_links(limit: int = 200, polite: bool = True) -> List[str]:
    """Crawl HackerNews website for fresh tech article links

    Args:
        limit (int, optional): Limits how much articles should be fetched. Defaults to 200.
        polite (bool, optional): Determine if crawling should be done politely according to robots.txt. Defaults to True.

    Returns:
        urls: Array of urls
    """
    base_url = "https://news.ycombinator.com"
    delay = 0
    pages = ceil(limit / 30)

    if polite:
        rp = RobotFileParser(url=f'{base_url}/robots.txt')
        rp.read()
        crawl_delay = rp.crawl_delay('*')

        if crawl_delay is None:
            crawl_delay = 0
        
        delay = int(crawl_delay)

    resp_body = []
    page = 1

    if delay == 0:
        urls = []

        while page <= pages:
            urls.append(f'{base_url}/news?p={page}')
            page += 1

        req = (grequests.get(url) for url in urls)
        
        for resp in grequests.imap(req):
            resp_body.append(resp.text)
    else:
        while page <= pages:
            resp = requests.get(f'{base_url}/news?p={page}')
            
            resp_body.append(resp.text)
            page += 1

            sleep(randint(delay, delay + 10)) # Simulate 'humans' access time

    urls = []

    for body in resp_body:
        body_parser = BeautifulSoup(body, 'html.parser')

        titles = body_parser.select('tr.athing .storylink')

        for title in titles:
            url = title.get('href')

            if not url.startswith('http'):
                url = f'{base_url}/{url}'
            
            if not url.endswith('.pdf'):
                urls.append(url)

    return urls

def crawl_hn_for_news(limit = 200, polite = True) -> CrawlingResult:
    """Crawl HackerNews website for fresh tech articles

    Args:
        limit (int, optional): Limits how much articles should be fetched. Defaults to 200.
        polite (bool, optional): Determine if crawling should be done politely according to robots.txt. Defaults to True.

    Returns:
        CrawlingResult: Crawler results, with timestamp
    """

    urls = _get_news_links(limit, polite)
    config = Config()
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

    return CrawlingResult(
        news=result,
        time=datetime.now(),
    )