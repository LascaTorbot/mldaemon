#!/usr/bin/python3
from config import *
from mldaemon.dataset.dataset import *
from mldaemon.dataset.dict import *
from mldaemon.utils.logger import Logger
from mldaemon.ml import MLDaemon
import time

while True:
    logger = Logger(LOG_PATH)

    # fit algorithms
    ml = MLDaemon(MONGO_HOST, MONGO_PORT, DATABASE_PATH, OUTPUT_PATH, logger, gen_dict=False)
    ml.test()

    logger.flush()

    print('sleep %d' % SLEEP_TIME)
    time.sleep(SLEEP_TIME)
