from config import *
from mldaemon.dataset.dataset import *
from mldaemon.dataset.dict import *
from mldaemon.utils.logger import Logger

logger = Logger(LOG_PATH)

# gen dict
dictionary = Dictionary(MONGO_HOST, MONGO_PORT, logger)
dictionary.gen_dict(DATABASE_PATH)

# gen dataset
dataset = Dataset(MONGO_HOST, MONGO_PORT, DATABASE_PATH, logger)
X, y = dataset.get_dataset()
print()
print(X)
print(y)

logger.flush()
