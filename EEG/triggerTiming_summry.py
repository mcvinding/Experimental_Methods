# -*- coding: utf-8 -*-
"""
Created on Thu May  8 10:42:26 2025
@author: ncb623
"""

import mne

fname = 'C:/Users/ncb623/experimental_methods/EEG/data/triggertiming20250508.bdf'

raw = mne.io.read_raw(fname)
eve = mne.find_events(raw)

epo = mne.Epochs(raw, tmin=-0.05, tmax=0.2, events=eve)

epo['1'].plot()
epo['1'].average().plot()
epo['1'].plot_image()
