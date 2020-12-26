from src import crawler

def main():
    result = crawler.crawl_hn_for_news(limit=90, polite=False)
    result.write_result_to_file()

if __name__ == "__main__":
    main()