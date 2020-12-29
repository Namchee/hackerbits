from nltk import word_tokenize
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from pandas import DataFrame
from re import search
from typing import List

from src.model.news import News

def k_means(news: List[News], clusters: int):
    tf_idf = _tf_idf(news)

    model = KMeans(n_cluster=clusters)

    model.fit(tf_idf)

    """

    wiki_cl = DataFrame(list(zip(title,labels)),columns=['title','cluster'])
    print(wiki_cl.sort_values(by=['cluster']))
    """

def get_clusters_with_elbow():
    return None

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

    tokens = list(filter(lambda token: token not in stopwords.words('english', tokens)))
    
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

    texts = list(map(lambda news: news.content, news_list))

    return vectorizer.fit_transform(texts)
