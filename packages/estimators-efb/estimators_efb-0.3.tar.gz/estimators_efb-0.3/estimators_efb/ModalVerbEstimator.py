import sys
import numpy as np
import nltk
from nltk.tokenize import word_tokenize
from sklearn.base import BaseEstimator, TransformerMixin

# Defining modal verb counter estimator to create new feature:
class ModalVerbCounter(BaseEstimator, TransformerMixin):
    '''
    Customized transformer for counting modal verbs occurances in text.
    '''
    # Adding 'activate' parameter to activate the transformer or not:
    def __init__(self, activate = True):
        self.activate = activate

    # Defining fit method:
    def fit(self, X, y = None):
        return self

    # Defining transform method:
    def transform(self, X):
        '''
        It recieves an array of messages and counts the number of modal verbs
        for each message.

        Input:
        X: array of text messages

        Output:
        n_md_arr: array with the number of modal verbs for each message
        '''
        # If activate parameter is set to True:
        if self.activate:
            # Creating empty list:
            n_md_list = list()
            # Counting modal verbs:
            for text in X:
                n_md = 0
                tokens = word_tokenize(text.lower())
                for tok, pos in nltk.pos_tag(tokens):
                    if pos == 'MD':
                        n_md += 1
                n_md_list.append(n_md)
            # Transforming list into array:
            n_md_arr = np.array(n_md_list)
            n_md_arr = n_md_arr.reshape((len(n_md_arr),1))
            return n_md_arr

        # If activate parameter is set to False:
        else:
            pass
