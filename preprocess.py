import pandas as pd
import os
import mne

def preprocess_ern(path, sfreq):

    for filename in os.listdir(path):
        f = os.path.join(path, filename)

        dataframe = pd.read_csv(f, delimiter=',')
        dataframe.drop(dataframe.columns[[0]], axis=1, inplace=True) 

        #From the link above - there is more info on how to define channel type etc for info structure
        n_channels = len(dataframe.columns)
        ch_names = dataframe.columns.values.tolist()   
        dataframe = dataframe.T

        sampling_freq = sfreq  # in Hertz - This is in the first line of the CSV
        info = mne.create_info(ch_names, sfreq=sampling_freq)
        raw = mne.io.RawArray(dataframe.values, info)  

        #...preprocessing ...
        raw.save(f[:-4] + '.raw.fif')


def bci_change_names(path):
    for filename in os.listdir(path):
        f = os.path.join(path, filename)

        new_name = ''
        if f[-5] == 'E':
            new_name = f[:-5] + '1' + f[-4:]
        elif f[-5] == 'T':
            new_name = f[:-5] + '2' + f[-4:]

        os.rename(f, new_name)
        

# bci_change_names("../datasets/bci_2a")
raw = mne.io.read_raw("../datasets/bci_2a/A011.gdf")
print(raw.ch_names)
