"""
Configuration file for MLDaemon
"""

from sklearn.decomposition import PCA, FactorAnalysis
from sklearn import tree, svm, preprocessing
from sklearn.naive_bayes import GaussianNB, MultinomialNB
from sklearn.neural_network import MLPClassifier
import os

MONGO_HOST = "127.0.0.1"
MONGO_PORT = 27017

DATABASE_PATH = '/home/aquari/mldaemon/database'
OUTPUT_PATH = '/home/aquari/mldaemon/output'
LOG_PATH = '/home/aquari/mldaemon/log'

# ML Algorithms configurations

cv = 10
dim_inic = 1000
dim_max = 6000
steps = 1000
apply_pca = False
decomposition_class = PCA

output_json_file = os.path.join(OUTPUT_PATH, 'output.json')

# instantiating classifiers
clfs = [
    ('Decision Tree', tree.DecisionTreeClassifier(), os.path.join(OUTPUT_PATH, 'tree.pkl')),
    ('Gaussian Naive Bayes', GaussianNB(), os.path.join(OUTPUT_PATH, 'gnb.pkl')),
    ('Neural Network MLP', MLPClassifier(solver='lbfgs', alpha=1e-5,
                           hidden_layer_sizes=(15,), random_state=1), os.path.join(OUTPUT_PATH, 'nnmlp.pkl')),
    ('Linear SVM', svm.SVC(kernel='linear', C=1), os.path.join(OUTPUT_PATH, 'lsvm.pkl')),
]
