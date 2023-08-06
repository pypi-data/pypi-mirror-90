import sys
import numpy as np
import nltk
from nltk.tokenize import word_tokenize
from sklearn.base import BaseEstimator, TransformerMixin

# Defining numeral counter estimator to create new feature:
class NumeralCounter(BaseEstimator, TransformerMixin):
    '''
    Customized transformer for counting numeral occurances in text.
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
        It recieves an array of messages and counts numeral occurances for each
        message.

        Input:
        X: array of text messages

        Output:
        n_cd_arr: array with the number of numeral occurances for each message
        '''
        # If activate parameter is set to True:
        if self.activate:
            # Creating empty list:
            n_cd_list = list()
            # Counting numeral occurances:
            for text in X:
                n_cd = 0
                tokens = word_tokenize(text.lower())
                for tok, pos in nltk.pos_tag(tokens):
                    if pos == 'CD':
                        n_cd += 1
                n_cd_list.append(n_cd)
            # Transforming list into array:
            n_cd_arr = np.array(n_cd_list)
            n_cd_arr = n_cd_arr.reshape((len(n_cd_arr), 1))
            return n_cd_arr

        # If activate parameter is set to False:
        else:
            pass
