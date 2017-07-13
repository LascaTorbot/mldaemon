from mldaemon.build_model import *
from mldaemon.dataset.dataset import Dataset
from mldaemon.config import *

print("Loading dataset...")
dataset = Dataset(MONGO_HOST, MONGO_PORT, DATABASE_PATH)
X, y = dataset.get_dataset()
print("Success!")

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
