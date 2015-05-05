import os                                                                                               
from src import data_io
import shelve
from contextlib import closing


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
    for auction_id in botted_auctions:
        auct = auctions_d[auction_id]
        auct_bids_id = auct.bids
        with closing(shelve.open(bids_shelf_path, protocol=2)) as bids_db:
            bids = [bids_db[bid_id] for bid_id in auct_bids_id]
        bidders_id = [bid.bidder_id for bid in bids]

