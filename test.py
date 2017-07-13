from config import *
from mldaemon.dataset.dataset import *
from mldaemon.dataset.dict import *

# gen dict
dictionary = Dictionary(MONGO_HOST, MONGO_PORT)
#dictionary.gen_dict(DATABASE_PATH)

# gen dataset
dataset = Dataset(MONGO_HOST, MONGO_PORT, DATABASE_PATH)
X, y = dataset.get_dataset()
print()
print(X)
print(y)
