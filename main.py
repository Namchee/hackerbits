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
    result = crawler.crawl_hn_for_news(limit=200, polite=False)

    clusterer = clustering.NewsClusterer(result.news)

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