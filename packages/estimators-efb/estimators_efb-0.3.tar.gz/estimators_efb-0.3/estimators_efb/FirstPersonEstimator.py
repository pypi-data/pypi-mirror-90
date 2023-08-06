import sys
import numpy as np
from nltk.tokenize import word_tokenize
from sklearn.base import BaseEstimator, TransformerMixin

# Defining first person pronoun estimator to create new feature:
class StartsWithFirstPersonPron(BaseEstimator, TransformerMixin):
    '''
    Customized transformer to check if the message starts with a first person
    pronoun.
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
        It recieves an array of messages and evaluates whether each message
        starts with one of the first person pronouns (I, my, we, our).

        Input:
        X: array of text messages

        Output:
        first_person_arr: array indicating whether each message starts with
        first person pronoun
        '''
        # If activate parameter is set to True:
        if self.activate:
            # Creating empty list:
            first_person = list()
            # Creating list to target first person pronouns:
            pron_list = ['i', 'my', 'we', 'our']
            # Tokenizing message and verifying whether first token is a first
            # person pronoun in the list or not:
            for text in X:
                tokens = word_tokenize(text.lower())
                if len(tokens) > 0:
                    if tokens[0] in pron_list:
                        first_person.append(1)
                    else:
                        first_person.append(0)
                else:
                    first_person.append(0)
            # Transforming list into array:
            first_person_arr = np.array(first_person)
            first_person_arr = first_person_arr.reshape((len(first_person_arr),1))
            return first_person_arr

        # If activate parameter is set to False:
        else:
            pass
