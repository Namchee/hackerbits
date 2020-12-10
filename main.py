from src import crawler

def main():
    result = crawler.crawl_hn(polite=False)

    result.write_result_to_file()

if __name__ == "__main__":
    main()