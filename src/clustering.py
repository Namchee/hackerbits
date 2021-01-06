from nltk import word_tokenize
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from pandas import DataFrame
from re import search
from typing import List

from src.model.news import News

def _tokenize(text: str) -> List[str]:
    """Generate tokens from a long text

    Args:
        text (str): Text to be processed.

    Returns:
        List[str]: List of tokens
    """
    tokens = word_tokenize(text)
    tokens = [token.lower() for token in tokens]

    stemmer = PorterStemmer()
    tokens = [stemmer.stem(token) for token in tokens]

    tokens = list(filter(lambda token: token not in stopwords.words('english'), tokens))
    
    tokens = list(filter(lambda token: search("[^a-zA-Z-]+", token) is None, tokens))

    return tokens

def _tf_idf(news_list: List[News]):
    """Generate tf-idf matrix from list of news

    Args:
        news_list (List[News]): List of news

    Returns:
        csr_matrix: tf-idf matrix
    """
    vectorizer = TfidfVectorizer(
        tokenizer=_tokenize,
        sublinear_tf=True,
    )

    texts = list(map(lambda news: news.contents, news_list))

    return vectorizer.fit_transform(texts)

def _silhouette_method(news) -> int:
    """Get optimum number of cluster using silhoutte method

    Returns:
        int: Optimum number of cluster
    """
    K = range(2,15)
    silhoutte_metric_score = []
    for k in K:
        kmeans = KMeans(n_clusters=k).fit(news)
        labels = kmeans.labels_
        silhoutte_metric_score.append(silhouette_score(news, labels))

    max_index = silhoutte_metric_score.index(max(silhoutte_metric_score))
    return max_index + 2



def k_means(news: List[News], clusters = None) -> None:
    """Cluster HackerNews' articles using K-Means

    Args:
        news (List[News]): List of HN's articles
        clusters (int, optional): Number of desired cluster. Defaults to _elbow_method().
    """
    tf_idf = _tf_idf(news)

    if clusters is None:
        clusters = _silhouette_method(tf_idf)
        print(clusters)

    km = KMeans(n_clusters=clusters)

    km.fit(tf_idf)

    results = DataFrame()
    results['news'] = list(map(lambda x: x.title, news))
    results['category'] = km.labels_

    print(results)
