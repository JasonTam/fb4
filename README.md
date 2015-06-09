# fb4

Features
=======
Simple stats (mean, std, min, max) computed over the following features:

* Diversity
  * # unique counties, devices, ips, (countries, devices), (countries, ips), (devices, ips) per auction

* Streaks
  * longest streak of the same device, ip, (device, ip) per auction

* Peak
  * for overlapping time windows:
    * # of bids in a given window
    * # of auctions in a given window
    * # unique auctions in the argmax window

* Count-Vectors
    * count vectors for each unique device, country, merch

* First Last
  * # instances a bidder submitted the first, last bid of an auction

* Consecutive
  *  # instances that a bidder has 0, 1, 2, ..., 10 bids in between their bids

* Wavelets
  * 3-level db4 wavelet decomposition for 3 overlapping windowed histograms of # of bids
    * |mean|, std of coefficients
    * differences in |mean|, std of coefficients between windows

* Time Difference
  * time since previous bid

* Position
  * # of bids in windows relative to auction life

Model
=====
Simple average of extra-trees, gradient boosted trees, neural net.

Other
=====
I always try semi-supervised learning... and it never helps my CV or LB score. =[

Score
=====
* CV:      ~0.92, 0.93, 0.91 (for the respective models)
* Public:  0.91503 (138)
* Private: 0.93649 (20)
