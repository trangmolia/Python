import csv
import string
from bayes import NaiveBayesClassifier

from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer


model_test = Pipeline([
    ('vectorizer', TfidfVectorizer()),
    ('classifier', MultinomialNB(alpha=1)),
])


def clean(s):
    translator = str.maketrans("", "", string.punctuation)
    return s.translate(translator)


def read_and_process_data():
    with open("./data/SMSSpamCollection") as f:
        data = list(csv.reader(f, delimiter="\t"))
    X, y = [], []
    for target, msg in data:
        X.append(msg)
        y.append(target)
    X = [clean(x).lower() for x in X]
    return X[:3900], y[:3900], X[3900:], y[3900:]


if __name__ == "__main__":
    X_train, y_train, X_test, y_test = read_and_process_data()

    model = NaiveBayesClassifier(alpha=1)
    model.fit(X_train, y_train)
    result_1 = model.score(X_test, y_test)

    model_test.fit(X_train, y_train)
    result_2 = model_test.score(X_test, y_test)

    print("Ok") if result_1 == result_2 else print("Failed")
