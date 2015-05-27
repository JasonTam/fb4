import numpy as np
import cPickle as pickle
from src import data_io
from src.containers import *
from contextlib import closing
import shelve
import os
from itertools import groupby

# ## Macro features
# behavioral change of micro features over a macro scale
# (bots do not change behavior on a macro scale)

# ## Micro features
# Bids per auction
# Time of bids relative to life of auction
# Categories of interest?
# device used to make early bids/ late bids

# For a given auction with a KNOWN bot,
# we hypothesize that the bot will snipe the auction with
# a last second bid - so this timestamp is assumed
# to be the last second of the auction
# We can classify snipers as the bidders who also
# bid in the last second (given that the auction contained a
# true bot)
# Though sniping behavior does not necessarily mean a bidder
# is a bot


# Number of bids per auction won
# number of bids per auction lost
# maybe count consecutive bids as 1

# number of unique devices/IP's/country per auction (maybe scaled by number of bids))

# win rate

# number of bids in a given window

from sklearn.base import BaseEstimator, TransformerMixin


class FitlessMixin(BaseEstimator, TransformerMixin):
    def fit_transform(self, X, y=None, **fit_params):
        self.fit(X, y, **fit_params)
        return self.transform(X)

    def fit(self, X, y=None, **fit_params):
        return self


class SnipeCounter():
    def __init__(self, bidder_ids, perc_thresh=0.95):
        """
        :param bidder_ids: the bidder ids to account for
        """
        self.perc_thresh = perc_thresh
        self.snipe_counts = {bidder_id: 0 for bidder_id in bidder_ids}
    
    def update(bidder_ids, times):
        """
        :param bidder_ids: the bidder ids of the auction participants
            (this is a subset of the variable specified in initialization)
        """
        for ind in np.where(times > self.snipe_counts)[0]:
            self.snipe_counts[bidders_id[ind]] += 1
        
        
    def save(save_path=os.path.join(data_io.SAVED_DIR, 'snipe_counts.p')):
        pickle.dump(self.snipe_counts, open(save_path,'wb'))
        

        
#class BidCountFeats():
#    def __init__():
#        # load the required data to do the child tasks


class BidsPerAuct():
    def __init__(self):
        pass

    def transform(self, bidders):
        rets = []
        for bidder in bidders:
            if len(bidder.bids_by_auction.values()):
                nbids_per_auct = np.array([len(a) for a in bidder.bids_by_auction.values()])
                
                tot_bids = nbids_per_auct.sum() if len(nbids_per_auct) else 0
                avg_bids_per_auct = nbids_per_auct.mean() if len(nbids_per_auct) else 0.
                std_bids_per_auct = nbids_per_auct.std() if len(nbids_per_auct) else 0.
                n_aucts = len(bidder.bids_by_auction)
                
                ret = np.array([
                        tot_bids,
                        avg_bids_per_auct, 
                        std_bids_per_auct, 
                        n_aucts])
            else:
                ret = np.zeros(4)
                    
            rets.append(ret)
        rets = np.array(rets)
        return rets

    
class BidDiversity():
    def __init__(self, bids_df):
        self.bids_df = bids_df

    def transform(self, bidders, verbose=False):
        rets = []
        for ii, bidder in enumerate(bidders):
            if len(bidder.bids_by_auction.values()):
                bids_by_auct = np.array([
                        [Bid(**self.bids_df.loc[int(bid_id)]) 
                                        for bid_id in a]
                        for a in bidder.bids_by_auction.values()])
                diversity_feats = []

                for auct in bids_by_auct:

                    countries = [bid.country for bid in auct]
                    devices = [bid.device for bid in auct]
                    ips = [bid.ip for bid in auct]

                    n_bids = len(auct)

                    diversity = np.array([
                            len(set(countries)),
                            len(set(devices)),
                            len(set(ips)),
                            len(set(zip(countries, devices))),
                            len(set(zip(countries, ips))),
                            len(set(zip(devices, ips))),
                            get_streak(devices)[1],
                            get_streak(ips)[1],
                            get_streak(zip(devices, ips))[1],
                        ])/float(n_bids)

                    diversity_feats.append(diversity)
                diversity_feats = np.array(diversity_feats)
                ret = np.concatenate([
                        diversity_feats.mean(axis=0),
                #         diversity_feats.max(axis=0),
                        diversity_feats.min(axis=0),
                        diversity_feats.std(axis=0),
                        ])
            else:
                ret = np.zeros(27)
                    
            rets.append(ret)
            print '\r %d / %d' % (ii+1, len(bidders)),
        rets = np.array(rets)
        return rets
        
        
        
class PeakBids():
    # Peak number of bids and the diversity during that peak
    # Peak diversity can also be found in a period that is not during the peak bids
    # Should probably run this with various window sizes
    def __init__(self, bids_df, win_sz=1e10):
        self.bids_shelf_path = data_io.BIDS_SHELF_PATH
        self.bids_df = bids_df
        
        self.win_sz = win_sz
        self.step = win_sz/2.  # Half overlap

    def transform(self, bidders, verbose=False):
        # too lazy to replace
        step = self.step
        win_sz = self.win_sz
        
        rets = []
        for ii, bidder in enumerate(bidders):
            # If the bidder has bids... -_-
            if len(bidder.bids_by_auction.values()):
                all_bids = np.concatenate(bidder.bids_by_auction.values())
                
                #with closing(shelve.open(self.bids_shelf_path, protocol=2)) as bids_db:
                #    bids = [bids_db[bid_id] for bid_id in all_bids]
                bids = [Bid(**self.bids_df.loc[int(bid_id)]) 
                        for bid_id in all_bids]
                
                t = np.array([bid.time for bid in bids])
                aucts = [bid.auction_id for bid in bids]

                n_bids_in_win = [1]
                unique_aucts_in_win = [1]
                for win_start in range(int(t.min()//step*step), int((t.max()//step)*step), int(step)):
                    t_in_win = (t > win_start) & (t < win_start+win_sz)
                    aucts_in_win = [auct for auct, t_i in zip(aucts, t_in_win) if t_i]
                    n_bids_in_win.append(np.sum(t_in_win))
                    unique_aucts_in_win.append(len(set(aucts_in_win)))

                n_bids_in_win = np.array(n_bids_in_win)
                unique_aucts_in_win = np.array(unique_aucts_in_win)

                ret = np.array([
                        n_bids_in_win.max(),
                        np.std(n_bids_in_win),
                        unique_aucts_in_win[np.argmax(n_bids_in_win)],
                        unique_aucts_in_win[np.argmax(n_bids_in_win)]/float(n_bids_in_win.max()),
                        unique_aucts_in_win.max(),
                        unique_aucts_in_win.max()/float(n_bids_in_win[np.argmax(unique_aucts_in_win)]),
                    ])
            else:
                ret = np.zeros(6)
            
            rets.append(ret)
            
            if verbose:
                print '\r %d / %d' % (ii+1, len(bidders)),
            
        return np.array(rets)
    

def get_streak(l):
    """Gives the value of the longest streak and its streak length"""
    chains = []
    for v, c in groupby(l):
       val, count = v, sum(1 for ii in c)
       chains.append((val,count))
    chains = np.array(chains)
    streak = chains[np.argmax(np.array(chains), axis=0)[1], :]
    return streak[0], int(streak[1])


        
        
        