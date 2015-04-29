import numpy as np


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
