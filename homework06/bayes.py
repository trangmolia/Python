from math import log


# in this case, we use Naive Bayes with Laplace smoothing
class NaiveBayesClassifier:

    def __init__(self, alpha=1):
        # alpha is a parameter estimation with add 1 smoothing
        self.alpha = alpha
        self.word_list = []
        self.frequency_ham = self.frequency_spam = []
        self.probability_word_ham = self.probability_word_spam = []

    def fit(self, X, y):
        """ Fit Naive Bayes classifier according to X, y. """
        index = -1
        count_word_ham = 0
        count_msg_ham = 0
        for i in range(len(X)):
            flag_list = X[i].split()
            if y[i] == 'ham':
                count_msg_ham += 1
            for word in flag_list:
                if word not in self.word_list:
                    index += 1
                    self.word_list.append(word)
                    self.frequency_ham.append(0)
                    self.frequency_spam.append(0)
                    if y[i] == 'ham':
                        self.frequency_ham[index] = 1
                        count_word_ham += 1
                    if y[i] == 'spam':
                        self.frequency_spam[index] = 1
                else:
                    if y[i] == 'ham':
                        self.frequency_ham[index] += 1
                    if y[i] == 'spam':
                        self.frequency_spam[index] += 1

        # amount meaning amount of words
        amount = len(self.word_list)
        count_word_spam = amount - count_word_ham

        # 2 list below use Laplace smoothing
        for i in range(amount):
            value_ham = (self.frequency_ham[i] + self.alpha) / (count_word_ham + amount*self.alpha)
            value_spam = (self.frequency_spam[i] + self.alpha) / (count_word_spam + amount*self.alpha)
            self.probability_word_ham.append(value_ham)
            self.probability_word_spam.append(value_spam)

        self.probability_msg_ham = count_msg_ham / len(X)
        self.probability_msg_spam = 1 - self.probability_msg_ham


    def predict(self, X):
        """ Perform classification on an array of test vectors X. """
        p1 = p2 = 0
        count = 0

        for word in X:
            if word in self.word_list:
                index = self.word_list.index(word)
                if self.probability_word_ham == 0:
                    count += 1
                p1 += log(self.probability_word_ham[index])
                p2 += log(self.probability_word_spam[index])
        p1 += log(self.probability_msg_ham)
        p2 += log(self.probability_msg_spam)

        return p1, p2


    def score(self, X_test, y_test):
        """ Returns the mean accuracy on the given test data and labels. """
        count = 0
        for i in range(len(X_test)):
            flag_list = X_test[i].split()
            p1, p2 = self.predict(flag_list)
            if p1 > p2:
                label = 'ham'
            else:
                label = 'spam'
            if label == y_test[i]:
                count += 1
            else:
                print(i)
        print('...')
        return count / len(y_test)
