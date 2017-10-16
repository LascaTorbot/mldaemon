from sklearn.model_selection import KFold
from sklearn.metrics import confusion_matrix
from sklearn import tree, svm, preprocessing
from sklearn.naive_bayes import GaussianNB, MultinomialNB
from sklearn.neural_network import MLPClassifier
from sklearn.decomposition import PCA, FactorAnalysis
from threading import Thread
from queue import Queue
import json
import numpy as np
import pickle

# normalize the X matrix
def normalize(X):
    normalizer = preprocessing.Normalizer().fit(X)
    return normalizer.transform(X)

# function to train algorithm
def train(clf, kf, X, y, queue):
    tn = tp = fn = fp = 0

    for train, test in kf.split(X):
        X_train, X_test = X[train], X[test]
        y_train, y_test = y[train], y[test]

        clf.fit(X_train, y_train)
        conf = confusion_matrix(y_test, clf.predict(X_test), labels=[0, 1])
        tn += conf[0][0]
        fn += conf[1][0]
        tp += conf[1][1]
        fp += conf[0][1]

    total = tn + tp + fn + fp
    tn_rate = tn / (tn + fp)
    tp_rate = tp / (tp + fn)
    fn_rate = fn / (tp + fn)
    fp_rate = fp / (tn + fp)
    accuracy = (tp + tn) / total

    queue.put((tn_rate, tp_rate, fn_rate, fp_rate, accuracy))

def build(clfs, X, y, cv, logger):
    kf = KFold(n_splits=cv)

    threads = []
    results = []

    for name, clf, __ in clfs:
        logger.log("Training %s..." % name)

        q = Queue()
        thread = Thread(target=train, args=(clf, kf, X, y, q))
        thread.start()
        threads.append(thread)
        results.append(q)

    out_json = {}
    for i in range(len(threads)):
        threads[i].join()
        tn_rate, tp_rate, fn_rate, fp_rate, accuracy = results[i].get()
        
        name, clf, output_name = clfs[i]

        out_json[name] = {
            'tp': tp_rate,
            'tn': tn_rate,
            'fp': fp_rate,
            'fn': fn_rate,
            'accuracy': accuracy,
        }

        logger.log("%s finished!" % name)

        pickle.dump(clf, open(output_name, 'wb'))

    return out_json

def predict(clfs, X, y, logger):
    out_json = {}

    # get all clfs
    for c in clfs:
        clf = pickle.load(open(c[2], 'rb'))  
        print(clf)
