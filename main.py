from src import crawler

def main():
    crawler.extract_hn_news(polite=False)

if __name__ == "__main__":
    main()