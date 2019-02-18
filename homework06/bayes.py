word_list = []
frequency_ham = []
frequency_spam = []


# in this case, we use Naive Bayes with Laplace smoothing
class NaiveBayesClassifier:

    def __init__(self, alpha=1):
        # alpha is a parameter estimation with add 1 smoothing
        self.alpha = alpha

    def fit(self, X, y):
        """ Fit Naive Bayes classifier according to X, y. """
        index = -1
        for i in range(len(X)):
            flag_list = X[i].split()
            for word in flag_list:
                if word not in word_list:
                    index += 1
                    word_list.append(word)
                    frequency_ham.append(0)
                    frequency_spam.append(0)
                    if y[i] == 'ham':
                        frequency_ham[index] = 1
                    if y[i] == 'spam':
                        frequency_spam[index] = 1
                else:
                    if y[i] == 'ham':
                        frequency_ham[index] += 1
                    if y[i] == 'spam':
                        frequency_spam[index] += 1
        print(word_list)

    def predict(self, X):
        """ Perform classification on an array of test vectors X. """
        pass

    def score(self, X_test, y_test):
        """ Returns the mean accuracy on the given test data and labels. """
        pass
