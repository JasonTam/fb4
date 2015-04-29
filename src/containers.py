from collections import OrderedDict


class Bid(object):
    def __init__(self,
                 bid_id, bidder_id,
                 auction_id, merchandise,
                 device, time, country,
                 ip, url):
        self.bid_id = bid_id
        self.bidder_id = bidder_id
        self.auction_id = auction_id
        self.merchandise = merchandise
        self.device = device
        self.time = time
        self.country = country
        self.ip = ip
        self.url = url

        # Pointers
        self.bidder = None
        self.auction = None

    def __str__(self):
        return self.bid_id


class Auction(object):
    """ A item for auction
    """
    def __init__(self, auction_id):
        self.auction_id = auction_id
        self.participants = None
        self.bids = None

        # Main merchandise category (mode)
        self.merchandise = None
        # Range from first to last bid
        self.active_range = None

    def add_bid(self, bid):
        pass
        # add bid to list (keep order by time)
        # update the active range

    def __str__(self):
        return self.auction_id


class Bidder(object):
    def __init__(self, bidder_id,
                 # payment_account, address,
                 outcome=None):
        self.bidder_id = bidder_id

        self.true_outcome = outcome  # 0=Human, 1=Bot
        self.pred_outcome = None

        # Auctions participated in (sorted by time)
        self.bids_by_auction = OrderedDict()

    def add_bid(self, bid):
        # Ghetto ordered default dict
        if bid.auction not in self.bids_by_auction.keys:
            self.bids_by_auction[bid.auction] = []
        self.bids_by_auction[bid.auction].append(bid)


    def __str__(self):
        return '\t'.join([
            self.bidder_id,
            str(self.true_outcome)])
