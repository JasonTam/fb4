from src import data_io
from src.containers import *
import numpy as np


make_bidder_train = lambda bidder_row: Bidder(
    bidder_row['bidder_id'], bidder_row['outcome'])
make_bidder_test = lambda bidder_row: Bidder(
    bidder_row['bidder_id'])

if __name__ == '__main__':
    train_df = data_io.load_train()
    bidders_d = {bidder.bidder_id: bidder
                 for bidder in train_df.apply(make_bidder_train, axis=1)}


