from urllib.robotparser import RobotFileParser
from bs4 import BeautifulSoup
from math import ceil
from os import getcwd
from datetime import datetime
from time import sleep
from json import dump
import grequests
import requests

class CrawlingResult:
    def __init__(self, articles, time: datetime):
        self.articles = articles
        self.time = time

    def write_result_to_file(self, dir = getcwd(), name = 'crawling_result'):
        """Write crawling result to a JSON file

        Args:
            dir (str, optional): Directory to be written. Defaults to getcwd().
            name (str, optional): File name. Defaults to 'crawling_result'.
        """
        with open(f'{dir}/{name}.json', 'w') as file:
            data = {}

            data['timestamp'] = self.time.isoformat()
            data['articles'] = self.articles

            dump(data, file, indent=4, sort_keys=True)

def crawl_hn(limit = 200, polite = True) -> CrawlingResult:
    """Crawl HackerNews website for fresh tech articles

    Args:
        limit (int, optional): Limits how much articles should be fetched. Defaults to 200.
        polite (bool, optional): Determine if crawling should be done politely according to robots.txt. Defaults to True.

    Returns:
        CrawlingResult: Crawler results, with timestamp
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

            sleep(delay)

    data_time = datetime.now()
    articles = []

    for body in resp_body:
        body_parser = BeautifulSoup(body, 'html.parser')
        titles = body_parser.select('tr.athing .storylink')

        for title in titles:
            url = title.get('href')

            if not url.startswith('http'):
                url = f'{base_url}/{url}'

            articles.append({
                'title': title.get_text(),
                'url': url
            })

    return CrawlingResult(
        articles=articles,
        time=data_time
    )
