import csv
import os
import pandas as pd
import cPickle as pickle
import gzip
import shelve

CURDIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(CURDIR, '../data')
SUBS_DIR = os.path.join(CURDIR, '../submissions')
SAVED_DIR = os.path.join(CURDIR, '../saved')
TRAIN_PATH = os.path.join(DATA_DIR, 'train.csv')
TEST_PATH = os.path.join(DATA_DIR, 'test.csv')
BIDDERS_AUCTIONS_PATH = os.path.join(SAVED_DIR, 'bidders_auctions.pgz')
BIDS_PATH = os.path.join(DATA_DIR, 'bids.csv')
SMALL_BIDS_PATH = os.path.join(DATA_DIR, 'small_bids.csv')
BIDS_SHELF_PATH = '/media/raid_arr/data/fb4/bids.db'


def load_bids(small=False):
    # maybe consider reading with index_col=0?
    
    # Make bid_id a str so that we can use it as shelve key
    readcsv = lambda p: pd.io.parsers.read_csv(p, dtype={'bid_id':str})
    if small:
        bids_df = readcsv(SMALL_BIDS_PATH)
    else:
        bids_df = readcsv(BIDS_PATH)
    return bids_df.fillna('nan')  # Replace NaN float with 'nan' str


def load_train():
    return pd.io.parsers.read_csv(TRAIN_PATH)


def load_test():
    return pd.io.parsers.read_csv(TEST_PATH)


def save_encoders(enc_dict, name='encoders.p'):
    p = os.path.join(SAVED_DIR, name)
    pickle.dump(enc_dict, open(p, 'wb'))
    return p


def load_encoders(name='encoders.p'):
    p = os.path.join(SAVED_DIR, name)
    return pickle.load(open(p, 'rb'))


def load_bidders_auctions():
    # p = os.path.join(SAVED_DIR, 'bidders_auctions.p')
    # p = os.path.join('/media/raid_arr/data/fb4/bidders_auctions.p')
    # return pickle.load(open(p, 'rb'))
    return pickle.load(gzip.open(BIDDERS_AUCTIONS_PATH, 'rb'))


def shelve_bid(bid, db):
    """ Shelve a bid object
    MUST be called in a `with shelve.open(***) as db` wrapper
    rather than inside this function
    :param bid: bid object
    :param db: db to shove into
    """
    db[bid.bid_id] = bid
