import csv
import os
import pandas as pd

CURDIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(CURDIR, '../data')
SUBS_DIR = os.path.join(CURDIR, '../submissions')
TRAIN_PATH = os.path.join(DATA_DIR, 'train.csv')
TEST_PATH = os.path.join(DATA_DIR, 'test.csv')
BIDS_PATH = os.path.join(DATA_DIR, 'bids.csv')
SMALL_BIDS_PATH = os.path.join(DATA_DIR, 'small_bids.csv')


def load_bids(small=False):
    if small:
        return pd.io.parsers.read_csv(SMALL_BIDS_PATH)
    else:
        return pd.io.parsers.read_csv(BIDS_PATH)


def load_train():
    return pd.io.parsers.read_csv(TRAIN_PATH)

def load_test():
    return pd.io.parsers.read_csv(TEST_PATH)