import unicodedata
import re
import nltk
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.corpus import stopwords
import pandas as pd
import acquire

def basic_clean(string):
    lower = string.lower()
    normal = unicodedata.normalize('NFKD', lower)\
        .encode('ascii', 'ignore')\
        .decode('utf-8', 'ignore')
    clean = re.sub(r"[^a-z0-9\s]", '', normal)
    return clean

def tokenize(string):
    string = basic_clean(string)
    tokenizer = nltk.tokenize.ToktokTokenizer()
    tokenized = tokenizer.tokenize(string, return_str=True)
    return tokenized

def stem(string):
    string = basic_clean(string)
    string = tokenize(string)
    ps = nltk.porter.PorterStemmer()
    stems = [ps.stem(word) for word in string.split()]
    stemmed = ' '.join(stems)
    return stemmed

def lemmatize(string):
    string = basic_clean(string)
    string = tokenize(string)
    wnl = nltk.stem.WordNetLemmatizer()
    lemmas = [wnl.lemmatize(word) for word in string.split()]
    lemmatized = ' '.join(lemmas)
    return lemmatized

def remove_stopwords(string, extra_words=[], exclude_words=[]):
    string = basic_clean(string)
    string = tokenize(string)
    stopword_list = stopwords.words('english')
    stopword_list += extra_words
    stopword_list = list(set(stopword_list) - set(exclude_words))
    words = string.split()
    filtered_words = [w for w in words if w not in stopword_list]
    string_without_stopwords = ' '.join(filtered_words)
    return string_without_stopwords

def prepare_article_data(df):
    df['stemmed'] = df.content.apply(stem)
    df['lemmatized'] = df.content.apply(lemmatize)
    df['clean'] = df.lemmatized.apply(remove_stopwords)
    return df