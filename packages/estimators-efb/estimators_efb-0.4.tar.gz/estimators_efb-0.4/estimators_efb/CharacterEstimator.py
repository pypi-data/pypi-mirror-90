import sys
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

# Defining character counter estimator to create new feature:
class CharacterCounter(BaseEstimator, TransformerMixin):
    '''
    Customized transformer for counting number of characters in text.
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
        n_caract: array with the number of characters for each message
        '''
        # If activate parameter is set to True:
        if self.activate:
            # Creating empty list:
            n_caract = list()
            # Counting characters:
            for text in X:
                n_caract.append(len(text))
            # Transforming list into array:
            n_caract = np.array(n_caract)
            n_caract = n_caract.reshape((len(n_caract),1))
            return n_caract

        # If activate parameter is set to False:
        else:
            pass
