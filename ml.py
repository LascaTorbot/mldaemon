from build_model import *

dataset_file = '../analysis/dataset/dataset.pkl'
cv = 5
dim_inic = 1000
dim_max = 6000
steps = 1000
apply_pca = True
decomposition_class = FactorAnalysis

output_json_file = 'output.json'

# instantiating classifiers
clfs = [
    ('Decision Tree', tree.DecisionTreeClassifier(), 'tree.pkl'),
    ('Gaussian Naive Bayes', GaussianNB(), 'gnb.pkl'),
#    ('Multinomial Naive Bayes', MultinomialNB(), 'mnb.pkl'),
    ('Neural Network MLP', MLPClassifier(solver='lbfgs', alpha=1e-5,
                               hidden_layer_sizes=(15,), random_state=1), 'nnmlp.pkl'),
    ('Linear SVM', svm.SVC(kernel='linear', C=1), 'lsvm.pkl'),
]

print("Loading dataset...")
dataset = pickle.load(open(dataset_file, 'rb'))
print("Success!")

# split into X and y vectors
X = []
y = []
for d in dataset:
    X.append(d[0])
    y.append(d[1])

X = np.array(X)
y = np.array(y)

print("Loaded %d samples..." % len(X))

print("Normalizing X matrix...")
X = normalize(X)
print("Success!")

out_json = {}

if apply_pca:
    dim = dim_inic
    while dim <= dim_max:
        print("Applying PCA for dimensionality %d..." % dim)
        pca = decomposition_class(n_components=dim)
        X_pca = pca.fit_transform(X)
        print("Success!\n")

        out = build(clfs, X_pca, y, cv)
        out_json[dim] = out

        dim += steps
        print("\n\n")

dim = len(X[0])
print("Without PCA, dimensionality %d..." % dim)
out = build(clfs, X, y, cv)
out_json[dim] = out

with open(output_json_file, 'w') as out_f:
    out_f.write(json.dumps(out_json, indent=4, sort_keys=True))
