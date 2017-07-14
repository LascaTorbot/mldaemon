from mldaemon.build_model import *
from mldaemon.dataset.dataset import Dataset
from mldaemon.dataset.dict import Dictionary
from mldaemon.config import *
import os

class MLDaemon:
    def __init__(self, MONGO_HOST, MONGO_PORT, DATABASE_PATH, OUTPUT_PATH, logger):
        self.logger = logger
        self.OUTPUT_PATH = OUTPUT_PATH

        self.logger.log('Instantiating dictionary...')
        self.dictionary = Dictionary(MONGO_HOST, MONGO_PORT, DATABASE_PATH, logger)
        self.logger.log('Done!')

        self.logger.log("Instantiating dataset...")
        self.dataset = Dataset(MONGO_HOST, MONGO_PORT, DATABASE_PATH, logger)
        self.logger.log("Done!")

    def fit(self):
        self.logger.log('Generating dictionaries...')
        self.dictionary.gen_dict()
        self.logger.log('Success!')

        self.logger.log('Loading dataset...')
        X, y = self.dataset.get_dataset()
        self.logger.log('Success!')

        self.logger.log("Loaded %d samples..." % len(X))

        self.logger.log("Normalizing X matrix...")
        X = normalize(X)
        self.logger.log("Success!")

        out_json = {}

        if apply_pca:
            dim = dim_inic
            while dim <= dim_max:
                self.logger.log("Applying PCA for dimensionality %d..." % dim)
                pca = decomposition_class(n_components=dim)
                X_pca = pca.fit_transform(X)
                self.logger.log("Success!\n")

                out = build(clfs, X_pca, y, cv, self.logger)
                out_json[dim] = out

                dim += steps

        dim = len(X[0])
        self.logger.log("Without PCA, dimensionality %d..." % dim)
        out = build(clfs, X, y, cv, self.logger)
        out_json[dim] = out

        with open(os.path.join(self.OUTPUT_PATH, 'out.json'), 'w') as out_f:
            out_f.write(json.dumps(out_json, indent=4, sort_keys=True))
