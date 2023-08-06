import sys
import numpy as np
from nltk.tokenize import word_tokenize
from sklearn.base import BaseEstimator, TransformerMixin

# Defining electricity words counter estimator to create new feature:
class ElectricityWordCounter(BaseEstimator, TransformerMixin):
    '''
    Customized transformer for counting number of electricity words in text.
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
        It recieves an array of messages and counts the number of characters
        for each message.

        Input:
        X: array of text messages

        Output:
        elec_words_arr: array with the number of electricity words for each
        message.
        '''
        # If activate parameter is set to True:
        if self.activate:
            elec_words_count = list()
            elec_list = ['electricity', 'power', 'energy', 'dark']
            # Counting electricity words:
            for text in X:
                # Creating empty list:
                elec_words = 0
                tokens = word_tokenize(text.lower())
                for word in tokens:
                    if word in elec_list:
                        elec_words += 1
                elec_words_count.append(elec_words)
            # Transforming list into array:
            elec_words_arr = np.array(elec_words_count)
            elec_words_arr = elec_words_arr.reshape((len(elec_words_arr), 1))
            return elec_words_arr

        # If activate parameter is set to False:
        else:
            pass
