from src import data_io
from src.containers import *
import numpy as np
from time import time


make_bidder_train = lambda bidder_row: Bidder(
    bidder_row['bidder_id'], bidder_row['outcome'])
make_bidder_test = lambda bidder_row: Bidder(
    bidder_row['bidder_id'])


def fill_bid(bid_row, auctions_d, bidders_d,
             verbose=True):
    bid = Bid(bid_id=bid_row['bid_id'],
              bidder_id=bid_row['bidder_id'],
              auction_id=bid_row['auction'],
              merchandise=bid_row['merchandise'],
              device=bid_row['device'],
              time=bid_row['time'],
              country=bid_row['country'],
              ip=bid_row['ip'],
              url=bid_row['url'],
              )
    if bid.auction_id not in auctions_d.keys():
        auctions_d[bid.auction_id] = Auction(bid.auction_id)
    auctions_d[bid.auction_id].add_bid(bid)

    try:
        bidders_d[bid.bidder_id].add_bid(bid)
    except KeyError:
        if verbose:
            print 'THERE IS A BID THAT HAS NO BIDDER'

    pass

if __name__ == '__main__':
    tic = time()
    train_df = data_io.load_train()
    test_df = data_io.load_test()
    bidders_d = {bidder.bidder_id: bidder
                 for bidder in train_df.apply(make_bidder_train, axis=1)}
    bidders_d.update(
        {bidder.bidder_id: bidder
         for bidder in test_df.apply(make_bidder_test, axis=1)})

    auctions_d = {}

    this_fill_bid = lambda bid_row: fill_bid(
        bid_row=bid_row,
        auctions_d=auctions_d,
        bidders_d=bidders_d)

    bids_df = data_io.load_bids(small=True)
    bids_df.apply(this_fill_bid, axis=1)

    toc = time() - tic
    print 'Total time: %g s' % toc