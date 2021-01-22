from os import getcwd, path
from sys import argv, exit
from nltk import download, data
from argparse import ArgumentParser, Namespace
from src import crawler, clustering
from json import load

def main() -> None:
    parser = ArgumentParser(description='Scrap HN and Cluster the results')
    
    parser.add_argument(
        'command',
        metavar='cmd',
        type=str,
        choices=['init', 'crawl', 'cluster'],
        help='Command to be executed'
    )
    parser.add_argument(
        '-c',
        '--count',
        metavar='limit',
        type=int,
        required=False,
        default=200,
        help='Number of documents to be scraped or clustered',
    )
    parser.add_argument(
        '-f',
        '--filename',
        metavar='name',
        type=str,
        required=False,
        default='crawling_result',
        help='Name of the file to be saved on or read from, will always relative to current project directory'
    )
    parser.add_argument(
        '-p',
        '--polite',
        dest='polite',
        action='store_true',
        help='Determine if the crawling should respect robots.txt or not, defaults to False',
    )
    parser.set_defaults(polite=False)

    parsed_args = parser.parse_args()
    cmd = parsed_args.command

    if cmd == "init":
        init()
    elif cmd == "crawl":
        crawl(parsed_args)
    else:
        cluster(parsed_args)

def init() -> None:
    nltk_path = path.join(getcwd(), 'venv', 'nltk_data')
    data.path.append(nltk_path)

    download('punkt', download_dir=nltk_path)
    download('stopwords', download_dir=nltk_path)

def crawl(args: Namespace) -> None:
    polite = args.polite
    filename = args.filename
    limit = args.count

    crawling_result = crawler.crawl_hn_for_news(limit=limit, polite=polite)

    crawling_result.write_result_to_file(name=filename)

def cluster(args: Namespace) -> None:
    filename = args.filename
    target = f'{getcwd()}/filename.json'

    has_crawled = path.exists(target)

    if has_crawled is False:
        print('Reference data not found, crawling websites...')

    with open(target, 'r') as file:
        crawling_result = load(file)
        news = crawling_result['news']

        clusterer = clustering.NewsClusterer(news)

        (flatLabelFour, fc_count) = clusterer.flat_clustering(4)
        (hierSingleFour, acs_count) = clusterer.agglomerative_clustering(4, linkage=clustering.Linkage.SINGLE)
        (hierCompleteFour, acc_count) = clusterer.agglomerative_clustering(4, linkage=clustering.Linkage.COMPLETE)
        (hierWardFour, acw_count) = clusterer.agglomerative_clustering(4, linkage=clustering.Linkage.WARD)
        (hierAverageFour, aca_count) = clusterer.agglomerative_clustering(4, linkage=clustering.Linkage.AVERAGE)

        print(clusterer.evaluate_result(flatLabelFour, clustering.EvaluationMethod.SILHOUETTE))
        print(clusterer.evaluate_result(hierSingleFour,clustering.EvaluationMethod.SILHOUETTE))
        print(clusterer.evaluate_result(hierCompleteFour, clustering.EvaluationMethod.SILHOUETTE))
        print(clusterer.evaluate_result(hierWardFour, clustering.EvaluationMethod.SILHOUETTE))
        print(clusterer.evaluate_result(hierAverageFour, clustering.EvaluationMethod.SILHOUETTE))

        clusterer.generate_wordcloud(flatLabelFour,fc_count,'4-fc','wc')
        clusterer.generate_wordcloud(hierSingleFour, acs_count,'4-ac-s','wc')
        clusterer.generate_wordcloud(hierCompleteFour,acc_count,'4-ac-c','wc')
        clusterer.generate_wordcloud(hierWardFour, acw_count,'4-ac-w','wc')
        clusterer.generate_wordcloud(hierAverageFour, aca_count,'4-ac-a','wc')

        (flatLabelTwo, fc_count) = clusterer.flat_clustering(2)
        (hierSingleTwo, acs_count) = clusterer.agglomerative_clustering(2, linkage=clustering.Linkage.SINGLE)
        (hierCompleteTwo, acc_count) = clusterer.agglomerative_clustering(2, linkage=clustering.Linkage.COMPLETE)
        (hierWardTwo, acw_count) = clusterer.agglomerative_clustering(2, linkage=clustering.Linkage.WARD)
        (hierAverageTwo, aca_count) = clusterer.agglomerative_clustering(2, linkage=clustering.Linkage.AVERAGE)

        print(clusterer.evaluate_result(flatLabelTwo, clustering.EvaluationMethod.SILHOUETTE))
        print(clusterer.evaluate_result(hierSingleTwo,clustering.EvaluationMethod.SILHOUETTE))
        print(clusterer.evaluate_result(hierCompleteTwo, clustering.EvaluationMethod.SILHOUETTE))
        print(clusterer.evaluate_result(hierWardTwo, clustering.EvaluationMethod.SILHOUETTE))
        print(clusterer.evaluate_result(hierAverageTwo, clustering.EvaluationMethod.SILHOUETTE))

        clusterer.generate_wordcloud(flatLabelTwo,fc_count,'2-fc','wc')
        clusterer.generate_wordcloud(hierSingleTwo, acs_count,'2-ac-s','wc')
        clusterer.generate_wordcloud(hierCompleteTwo,acc_count,'2-ac-c','wc')
        clusterer.generate_wordcloud(hierWardTwo, acw_count,'2-ac-w','wc')
        clusterer.generate_wordcloud(hierAverageTwo, aca_count,'2-ac-a','wc')

if __name__ == "__main__":    
    main()