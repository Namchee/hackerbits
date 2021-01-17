from os import getcwd, path
from sys import argv, exit
from nltk import download, data
from src import crawler, clustering

def main() -> None:
    if len(argv) != 2:
        print("This program requires exactly one argument: 'init' and 'cluster'")
        exit()

    cmd = argv[1]

    if cmd not in ['init', 'cluster']:
        print("This program only accepts 'init' and 'cluster' as the first argument")
        exit()

    if cmd == "init":
        init()
    else:
        cluster()

def init() -> None:
    nltk_path = path.join(getcwd(), 'venv', 'nltk_data')
    data.path.append(nltk_path)

    download('punkt', download_dir=nltk_path)
    download('stopwords', download_dir=nltk_path)

def cluster() -> None:
    result = crawler.crawl_hn_for_news(limit=90, polite=False)

    print(len(result.news))

    """
    clusterer = clustering.NewsClusterer(result.news)
    (labels, _) = clusterer.k_means()
    
    print(clusterer.evaluate_result(labels, clustering.EvaluationMethod.CALINSKI_HARABASZ))
    """

if __name__ == "__main__":    
    main()