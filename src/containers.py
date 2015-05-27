from collections import OrderedDict
from src.encoders import Encoders


class Bid(object):
    __slots__ = ['bid_id', 'bidder_id', 'auction_id',
                 'merchandise', 'device', 'time',
                 'country', 'ip', 'url',
                 'bidder', 'auction']

    def __init__(self,
                 bid_id, bidder_id,
                 auction, merchandise,
                 device, time, country,
                 ip, url):
        self.bid_id = bid_id
        self.bidder_id = bidder_id
        self.auction_id = auction
        self.merchandise = Encoders['merchandise'].transform((merchandise,))[0]
        self.device = device.replace('phone', '')
        self.time = time
        self.country = Encoders['country'].transform((country,))[0]
        self.ip = ip
        self.url = url

    def __str__(self):
        return self.bid_id


class Auction(object):
    """ A item for auction
    """
    __slots__ = ['auction_id', 'participants', 'bids',
                 'merchandise_list', 'merchandise', 'active_range']

    def __init__(self, auction_id):
        self.auction_id = auction_id
        self.participants = None
        self.bids = []

        self.merchandise_list = []
        # Main merchandise category (mode)
        self.merchandise = None
        # Range from first to last bid
        self.active_range = None

    def add_bid(self, bid):
        self.bids.append(bid.bid_id)
        # todo
        # add bid to list (keep order by time)
        # update the active range

    def __str__(self):
        return self.auction_id


class Bidder(object):
    __slots__ = ['bidder_id', 'true_outcome', 'pred_outcome',
                 'bids_by_auction']

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
        if bid.auction.auction_id not in self.bids_by_auction.keys():
            self.bids_by_auction[bid.auction.auction_id] = []
        self.bids_by_auction[bid.auction.auction_id].append(bid.bid_id)

    def __str__(self):
        return '\t'.join([
            self.bidder_id,
            str(self.true_outcome)])
