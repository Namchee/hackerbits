from enum import Enum
from typing import Any, Tuple
from nltk import word_tokenize
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
from scipy.sparse.csr import csr_matrix
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score
from re import search
from typing import List
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt

from src.model.news import News

class EvaluationMethod(Enum):
    """List of allowed clustering evaluation methods
    """
    SILHOUETTE = 1
    CALINSKI_HARABASZ = 2
    DAVIES_BOULDIN = 3

class Linkage(Enum):
    """List of allowed linkage for agglomerative clustering
    """
    WARD = 'ward'
    COMPLETE = 'complete'
    AVERAGE = 'average'
    SINGLE = 'single'

class NewsClusterer:
    """Clusterer for HackerNews' news articles
    """
    def __init__(self, news: List[News]) -> None:
        if len(news) < 15:
            raise ValueError('Jumlah berita minimum yang dapat diproses adalah sebanyak 15 berita')

        self.tf_idf = self._tf_idf(news)

    def _tokenize(_, text: str) -> List[str]:
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

    def _tf_idf(self, news: List[News]) -> csr_matrix:
        """Generate tf-idf matrix from list of news

        Args:
            news_list (List[News]): List of news

        Returns:
            csr_matrix: tf-idf matrix
        """
        vectorizer = TfidfVectorizer(
            tokenizer=self._tokenize,
            sublinear_tf=True,
        )

        texts = list(map(lambda news: news.contents, news))
        self.texts = texts
        return vectorizer.fit_transform(texts)    

    def _get_optimal_cluster_count(self,linkage=None) -> int:
        """Get optimum number of cluster using silhoutte method

        Returns:
            int: Optimum number of cluster
        """
        K = range(2,15)
        silhoutte_metric_score = []
        if linkage is None:
            for k in K:
                cluster = KMeans(n_clusters=k).fit(self.tf_idf)
                labels = cluster.labels_
                silhoutte_metric_score.append(silhouette_score(self.tf_idf, labels, metric='euclidean'))
        else:
            for k in K:
                cluster = AgglomerativeClustering(n_clusters=k,linkage=linkage).fit(self.tf_idf.toarray())
                labels = cluster.labels_
                silhoutte_metric_score.append(silhouette_score(self.tf_idf, labels, metric='euclidean'))

        max_index = silhoutte_metric_score.index(max(silhoutte_metric_score))

        return max_index + 2    

    def flat_clustering(self, cluster_count = None) -> Tuple[Any, int]:
        """Cluster HackerNews' articles using K-Means, a flat clustering method

        Args:
            news (List[News]): List of HN's articles
            clusters (int, optional): Number of desired cluster. Defaults to _get_optimal_cluster_count().

        Returns:
            Tuple(Any, int): Labels for each news item and how much clusters is used
        """
        if cluster_count is None:
            cluster_count = self._get_optimal_cluster_count()

        model = KMeans(n_clusters=cluster_count)

        model.fit(self.tf_idf)

        return (model.labels_, cluster_count)

    def agglomerative_clustering(self, cluster_count = None, linkage: Linkage = Linkage.SINGLE) -> Tuple[Any, int]:
        """Cluster HackerNews' articles using agglomerative hierarchical clustering

        Args:
            news (List[News]): List of HN's articles
            clusters (int, optional): Number of desired cluster. Defaults to _elbow_method().

        Returns:
            Tuple(Any, int): Labels for each news item and how much clusters is used
        """
        if cluster_count is None:
            cluster_count = self._get_optimal_cluster_count(linkage=linkage.value)
        model = AgglomerativeClustering(n_clusters=cluster_count,linkage=linkage.value)
        model.fit(self.tf_idf.toarray())

        return (model.labels_, cluster_count)


    def evaluate_result(self, labels: Any, method: EvaluationMethod) -> float:
        """Evaluate clustering result with an internal criteria

        Args:
            labels (Any): Labels for each news item
            method (EvaluationMethod): Evaluation method to be used. May be:
                1. Silhouette Coefficient
                2. Calinski-Harabasz Coefficient
                3. Davies Boulding Coefficient

            Although normally, you might want to use just Silhouette
            Please refer to the SKLearn documentation for more information
        Returns:
            float: Score for clustering result.
                For Silhouette and Calinski Harabasz, the higher the score, the better.
                For Davies Bouldin score, the lower the better.
                Will return `-1` if the evaluation method doesn't exist.
        """
        switcher = {
            1: silhouette_score,
            2: calinski_harabasz_score,
            3: davies_bouldin_score,
        }

        func = switcher.get(method.value)

        if func is None:
            return -1
        elif method.value == 1:
            return func(self.tf_idf, labels, metric='euclidean')
        else:
            return func(self.tf_idf.toarray(), labels)


    def generate_wordcloud(self, labels: Any, c_count: int, add_str: str, folder: str):
        """Generate word cloud for each cluster

        Args:
            labels (Any): Labels for each news item
            c_count (int): Number of clusters
            add_str (str): Additional string to differentiate file names
            folder (str): Target folder to generate word cloud picture files
        """
        result={'cluster':labels,'tx':self.texts}
        result=pd.DataFrame(result)
        for k in range(0,c_count):
            s = result[result.cluster==k]
            text = s['tx'].str.cat(sep=' ')
            text = text.lower()
            text =' '.join([word for word in text])
            wordcloud = WordCloud(max_font_size=50, max_words=100, background_color="white").generate(text)
            fig = plt.figure()
            plt.imshow(wordcloud, interpolation="bilinear")
            plt.axis("off")
            plt.savefig('wc/'+add_str+'-cluster'+str(k)+'.png'.format(folder))
            print("Generated "+'wc/'+add_str+'-cluster'+str(k)+'.png')
            plt.close(fig)
            
