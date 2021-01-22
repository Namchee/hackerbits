from collections import namedtuple
from os import getcwd, path
from timeit import default_timer
from nltk import download, data
from argparse import ArgumentParser, Namespace
from src import crawler, clustering
from json import load, loads

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
        metavar='count',
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

    if cmd == 'init':
        init()
    elif cmd == 'crawl':
        crawl(parsed_args)
    else:
        cluster(parsed_args)

def init() -> None:
    """Initalize sklearn by downloading required data
    """

    nltk_path = path.join(getcwd(), 'venv', 'nltk_data')
    data.path.append(nltk_path)

    download('punkt', download_dir=nltk_path)
    download('stopwords', download_dir=nltk_path)

def crawl(args: Namespace) -> None:
    """Crawl HackerNews for articles and save it to a file to be re-used later

    Args:
        args (Namespace): Passed command line arguments
    """
    polite = args.polite
    filename = args.filename
    limit = args.count

    start_time = default_timer()

    print(f'Crawling HackerNews for {limit} articles...')

    crawling_result = crawler.crawl_hn_for_news(limit=limit, polite=polite)

    crawling_result.write_result_to_file(name=filename)

    print(f'Successfully written data to {filename}.json')
    print(f'Finished crawling {limit} articles from HackerNews by {round(default_timer() - start_time, 3)} seconds')

def cluster(args: Namespace) -> None:
    """Cluster HackerNews articles with various algorithms.

    Args:
        args (Namespace): Passed command line arguments
    """
    filename = args.filename
    target = f'{getcwd()}/{filename}.json'

    has_crawled = path.exists(target)

    if has_crawled is False:
        print('Reference data not found, program will crawl HackerNews first.')
        crawl(args)
    with open(target, 'r') as file:
        crawling_result = load(file)
        news = crawling_result['news']

        fetched_at = crawling_result['fetched_at']

        news = list(map(lambda x: namedtuple('News', x.keys())(*x.values()), news))

        print(f'Begin clustering with data from {fetched_at}')

        clusterer = clustering.NewsClusterer(news)

        print('--- BEGIN CLUSTERING WITH 4 CLUSTERS --- ')

        start_fc_four = default_timer()

        (flatLabelFour, fc_count) = clusterer.flat_clustering(4)

        print(f'Finished clustering 200 documents with 4-Means in {round(default_timer() - start_fc_four, 3)} seconds')

        start_acs_four = default_timer() 

        (hierSingleFour, acs_count) = clusterer.agglomerative_clustering(4, linkage=clustering.Linkage.SINGLE)

        print(f'Finished clustering 200 documents with Agglomerative Single-Link Clustering with 4 clusters in {round(default_timer() - start_acs_four, 3)} seconds')

        start_acc_four = default_timer() 

        (hierCompleteFour, acc_count) = clusterer.agglomerative_clustering(4, linkage=clustering.Linkage.COMPLETE)

        print(f'Finished clustering 200 documents with Agglomerative Complete-Link Clustering with 4 clusters in {round(default_timer() - start_acc_four, 3)} seconds')

        start_acw_four = default_timer()

        (hierWardFour, acw_count) = clusterer.agglomerative_clustering(4, linkage=clustering.Linkage.WARD)

        print(f'Finished clustering 200 documents with Agglomerative Ward-Link Clustering with 4 clusters in {round(default_timer() - start_acw_four, 3)} seconds')

        start_aca_four = default_timer()

        (hierAverageFour, aca_count) = clusterer.agglomerative_clustering(4, linkage=clustering.Linkage.AVERAGE)

        print(f'Finished clustering 200 documents with Agglomerative Average-Link Clustering with 4 clusters in {round(default_timer() - start_aca_four, 3)} seconds')

        print(f'Silhouette score of FC: {clusterer.evaluate_result(flatLabelFour, clustering.EvaluationMethod.SILHOUETTE)}')
        print(f'Silhouette score of AC-S: {clusterer.evaluate_result(hierSingleFour,clustering.EvaluationMethod.SILHOUETTE)}')
        print(f'Silhouette score of AC-C: {clusterer.evaluate_result(hierCompleteFour, clustering.EvaluationMethod.SILHOUETTE)}')
        print(f'Silhouette score of AC-W: {clusterer.evaluate_result(hierWardFour, clustering.EvaluationMethod.SILHOUETTE)}')
        print(f'Silhouette score of AC-A: {clusterer.evaluate_result(hierAverageFour, clustering.EvaluationMethod.SILHOUETTE)}')

        print('--- END CLUSTERING WITH 4 CLUSTERS ---')

        clusterer.generate_wordcloud(flatLabelFour,fc_count,'4-fc','wc')
        clusterer.generate_wordcloud(hierSingleFour, acs_count,'4-ac-s','wc')
        clusterer.generate_wordcloud(hierCompleteFour,acc_count,'4-ac-c','wc')
        clusterer.generate_wordcloud(hierWardFour, acw_count,'4-ac-w','wc')
        clusterer.generate_wordcloud(hierAverageFour, aca_count,'4-ac-a','wc')

        print('--- BEGIN CLUSTERING WITH 2 CLUSTERS ---')

        (flatLabelTwo, fc_count) = clusterer.flat_clustering(2)
        (hierSingleTwo, acs_count) = clusterer.agglomerative_clustering(2, linkage=clustering.Linkage.SINGLE)
        (hierCompleteTwo, acc_count) = clusterer.agglomerative_clustering(2, linkage=clustering.Linkage.COMPLETE)
        (hierWardTwo, acw_count) = clusterer.agglomerative_clustering(2, linkage=clustering.Linkage.WARD)
        (hierAverageTwo, aca_count) = clusterer.agglomerative_clustering(2, linkage=clustering.Linkage.AVERAGE)

        print(f'Silhouette score of FC: {clusterer.evaluate_result(flatLabelTwo, clustering.EvaluationMethod.SILHOUETTE)}')
        print(f'Silhouette score of AC-S: {clusterer.evaluate_result(hierSingleTwo,clustering.EvaluationMethod.SILHOUETTE)}')
        print(f'Silhouette score of AC-C: {clusterer.evaluate_result(hierCompleteTwo, clustering.EvaluationMethod.SILHOUETTE)}')
        print(f'Silhouette score of AC-W: {clusterer.evaluate_result(hierWardTwo, clustering.EvaluationMethod.SILHOUETTE)}')
        print(f'Silhouette score of AC-A: {clusterer.evaluate_result(hierAverageTwo, clustering.EvaluationMethod.SILHOUETTE)}')

        clusterer.generate_wordcloud(flatLabelTwo,fc_count,'2-fc','wc')
        clusterer.generate_wordcloud(hierSingleTwo, acs_count,'2-ac-s','wc')
        clusterer.generate_wordcloud(hierCompleteTwo,acc_count,'2-ac-c','wc')
        clusterer.generate_wordcloud(hierWardTwo, acw_count,'2-ac-w','wc')
        clusterer.generate_wordcloud(hierAverageTwo, aca_count,'2-ac-a','wc')

        print('--- END CLUSTERING WITH 2 CLUSTERS ---')

if __name__ == "__main__":    
    main()