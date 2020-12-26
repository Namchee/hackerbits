from nltk import tokenize, word_tokenize
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from re import search
from typing import List

from src.model.news import News

def k_means(news: List[News]):
    return None

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
