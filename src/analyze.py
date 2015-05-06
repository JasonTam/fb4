import os                                                                                               
from src import data_io
import shelve
from contextlib import closing
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

if __name__ == '__main__':
    load = False
    if load:
        bidders_d, auctions_d = data_io.load_bidders_auctions()

    bots_id = {bidder_id for bidder_id, bidder in bidders_d.items() if bidder.true_outcome == 1.0}

    botted_auctions = set()

    for bot_id in bots_id:
        bot = bidders_d[bot_id]
        botted_auctions = botted_auctions.union(bot.bids_by_auction.keys())


    botted_sniped_auctions = set()
    bids_shelf_path = data_io.BIDS_SHELF_PATH
    durs = []
    for auction_id in botted_auctions:
        auct = auctions_d[auction_id]
        auct_bids_id = auct.bids
        with closing(shelve.open(bids_shelf_path, protocol=2)) as bids_db:
            bids = [bids_db[bid_id] for bid_id in auct_bids_id]
        bidders_id = [bid.bidder_id for bid in bids]

        times = np.array([b.time for b in bids])
        # Set Snipe threshold as 95 percentile of time??
        snipe_thresh = np.percentile(times, 95)
        # Or as some constant time before end

        auct_duration = times.max() - times.min()
        durs.append(auct_duration)

        # Should show a scatter plot of bids by time (colored by outcome)
        o = np.array([bidders_d[b.bidder_id].true_outcome for b in bids])
        c_d = {0.0: 'g', 1.0:'r', None: 'b'}
        colrs = [c_d[o_i] for o_i in o]

        plt.scatter(np.arange(len(times)), times, c=colrs, 
            s=100, lw=0, alpha=0.5)
        raw_input()




