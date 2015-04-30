import os
import pickle

from sklearn.preprocessing import LabelEncoder

from src import data_io


def make_encoders():
    bids_df = data_io.load_bids()
    enc_dict = {}
    enc_dict['country'] = LabelEncoder().fit(bids_df['country'])
    enc_dict['merchandise'] = LabelEncoder().fit(bids_df['merchandise'])
    save_path = data_io.save_encoder(enc_dict, 'encoders.p')
    return enc_dict
    
try:
    Encoders = data_io.load_encoders()
except IOError:
    Encoders = make_encoders()
