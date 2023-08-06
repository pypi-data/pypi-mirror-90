import sys
import numpy as np
import pandas as pd
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from sklearn.base import BaseEstimator, TransformerMixin

# Defining tokenizer estimator:
class TextTokenizer(BaseEstimator, TransformerMixin):
    '''
    Customized transformer for tokenizing text.
    '''
    # Adding 'activate' parameter to activate the transformer or not:
    def __init__(self, activate = True):
        self.activate = activate

    # Defining fit method:
    def fit(self, X, y = None):
        return self

    # Defining transform method:
    def transform(self, X):
        def tokenizer(text):
            '''
            It recieves an array of messages, and for each message: splits text into
            tokens, applies lemmatization, transforms to lowercase, removes blank
            spaces and stop-words.

            Input:
            X: array of text messages

            Output:
            tok_text: message after the transformations
            '''
            # Getting list of all urls using regex:
            detected_urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
            # Replacing each url in text string with placeholder:
            for url in detected_urls:
                text = text.replace(url, 'urlplaceholder')
            # Extracting tokens from text:
            tokens = word_tokenize(text)
            # Instantiating Lemmatizer object:
            lemmatizer = WordNetLemmatizer()
            # Applying transformations:
            clean_tokens = []
            for tok in tokens:
                # Lemmatizing, trnasforming to lowercase, and removing blank spaces:
                clean_tok = lemmatizer.lemmatize(tok).lower().strip()
                # Adding transformed token to clean_tokens list:
                clean_tokens.append(clean_tok)
            # Removing stopwords:
            stopwords_list = list(set(stopwords.words('english')))
            clean_tokens = [token for token in clean_tokens if token not in stopwords_list]
            # Return from tokenizer function:
            tok_text = ' '.join(clean_tokens)
            return tok_text
        if self.activate:
            # Return from transform method:
            return pd.Series(X).apply(tokenizer).values
        else:
            pass
