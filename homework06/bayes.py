from collections import Counter, defaultdict
from math import log
import numpy as np


# in this case, we use Naive Bayes with Laplace smoothing
class NaiveBayesClassifier:

    def __init__(self, alpha=0.05):
        # alpha is a parameter estimation with add 1 smoothing
        self.alpha = alpha

    def fit(self, X, y):
        """ Fit Naive Bayes classifier according to X, y. """

        # count all labels given from y
        self.labels = list(Counter(y).keys())

        # data is list of defaultdicts
        # each defaultdict has all words with frequency
        # labels[0] corresponds to data[0]
        self.data = []

        # amount_words is list of amount different words according labels
        self.amount_words = []

        # all_words is total different words trained
        self.all_words = 0

        for label in self.labels:
            d = defaultdict(int)
            for i in range(len(X)):
                if y[i] == label:
                    words = X[i].split()
                    for word in words:
                        d[word] += 1
            self.amount_words.append(len(d))
            self.all_words += len(d)
            self.data.append(d)

    def predict(self, X):
        """ Perform classification on an array of test vectors X. """
        result = ['']*len(X)
        label_index = 0

        for x in X:
            words = x.split()

            # proba_title is list of probabilities with each label
            proba_title = []

            for i in range(len(self.data)):
                proba = 0
                for word in words:
                    key = self.data[i].keys()
                    if word in key:
                        proba += log((self.data[i][word] + 1) / (self.amount_words[i] + self.all_words))
                    else:
                        proba += log(1 / (self.amount_words[i] + self.all_words))
                proba += log(self.amount_words[i] / self.all_words)
                proba_title.append(proba)
            index_max_proba = np.argmax(proba_title, axis=None, out=None)
            result[label_index] = self.labels[index_max_proba]
            label_index += 1

        return result

    def score(self, X_test, y_test):
        """ Returns the mean accuracy on the given test data and labels. """
        result = self.predict(X_test)
        count = 0
        for i in range(len(result)):
            if result[i] == y_test[i]:
                count += 1
        return count / len(y_test)
