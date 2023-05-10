import pandas as pd
import os
import mne
from glob import glob

bci_path = "/home/opc/datasets/bci_2a"
ern_path = "/home/opc/datasets/ern/train"
ssc_path = "/home/opc/datasets/physionet.org/files/sleep-edfx/1.0.0/sleep-cassette"
tuep_glob_path = glob('/home/opc/datasets/tuep/*/*/*/*/*.edf')

ern_train_t_path = "/home/opc/datasets/ern/train_t"
ern_preprocessed_path = "/home/opc/datasets/ern_preprocessed"
ern_train_labels = "/home/opc/datasets/ern/TrainLabels.csv"

sampling_freq = 256
bci_mapping = {
    'EEG-Fz': 'FZ',
    'EEG-0': 'FC3',
    'EEG-1': 'FC1',
    'EEG-2': 'FCZ',
    'EEG-3': 'FC2',
    'EEG-4': 'FC4',
    'EEG-5': 'C5',
    'EEG-C3': 'C3',
    'EEG-6': 'C1',
    'EEG-Cz': 'CZ',
    'EEG-7': 'C2',
    'EEG-C4': 'C4',
    'EEG-8': 'C6',
    'EEG-9': 'CP3',
    'EEG-10': 'CP1',
    'EEG-11': 'CPZ',
    'EEG-12': 'CP2',
    'EEG-13': 'CP4',
    'EEG-14': 'P1',
    'EEG-Pz': 'PZ',
    'EEG-15': 'P2',
    'EEG-16': 'POZ'
}

def ern_preprocess(path, labels_path):

    for filename in os.listdir(path):
        f = os.path.join(path, filename)

        # read files and drop the first column (Time)
        dataframe = pd.read_csv(f, delimiter=',')
        dataframe.drop(dataframe.columns[[0]], axis=1, inplace=True) 

        # set channel names
        ch_names = dataframe.columns.values.tolist()   

        # create info and raw objects
        # TODO add channel types to info
        info = mne.create_info(ch_names, sfreq=sampling_freq)
        raw = mne.io.RawArray(dataframe.T, info)

        # Set the last column, 'FeedBackEvent', and define it to be a stim (stimulus) channel
        raw.set_channel_types({'FeedBackEvent': 'stim'})
        events = mne.find_events(raw, stim_channel='FeedBackEvent') 

        # read the train labels
        feedback_df = pd.read_csv(labels_path, delimiter=',')
        feedback_df = feedback_df.reset_index()
        
        # change the event value in the third column
        for index, row in feedback_df.iterrows():
            if row['IdFeedBack'][:-6] == filename[5:-4]:
                fb_id = int(row['IdFeedBack'][14:16] if row['IdFeedBack'][13] == '0' else row['IdFeedBack'][13:16])
                events[fb_id-1][2] = int(row['Prediction']) + 1

        raw.add_events(events, stim_channel='FeedBackEvent', replace=True)
        mne.find_events(raw, stim_channel='FeedBackEvent') 

        # save the file
        mne.io.Raw.save(raw, filename[:-4] + '.raw.fif', overwrite=True)        


def bci_preprocess(path):
    for filename in os.listdir(path):
        f = os.path.join(path, filename)

        raw = mne.io.read_raw_gdf(f)

        # drop EOG channels
        raw.drop_channels(['EOG-central', 'EOG-right', 'EOG-left'])

        # renames the channels so that dn3 can read them
        raw.rename_channels(bci_mapping)

        # saves the files in .raw.fif format
        mne.io.Raw.save(raw, filename[:-4] + '.raw.fif', overwrite=True)
        

def ssc_preprocess(path):
    for filename in os.listdir(path):
        f = os.path.join(path, filename)

        # only preprocess the recordings
        if "Hypnogram" not in filename and not filename == 'index.html':
            # saves the files in .raw.fif format
            raw = mne.io.read_raw_edf(f)
            mne.io.Raw.save(raw, filename[:-4] + '.raw.fif', overwrite=True)


def tuep_preprocess(path):
    # Iterate through each file under the TUEP toplevel
    for file in path:
        print(file)
        # Read the raw file in .edf format. Specify stim channel as 'STI101).
        raw = mne.io.read_raw_edf(file, stim_channel='STI101', preload=True)
        # Only consider files where 'STI101' is not one of the channels already
        if 'STI101' not in raw.info['ch_names']:
                # Add 'STI101' as a 'reference channel'.
                raw.add_reference_channels('STI101')
                # Remove date - this is set to today by default, which is not correct.
                raw.set_meas_date(None)
                # Give files with 'no_epilepsy' in their file path an event '0'.
                if 'no_epilepsy' in file:
                        raw.add_events([[1, 0, 0]], stim_channel='STI101')
                # Give files with 'epilepsy' in their file path an event '1'.
                else:
                        raw.add_events([[1, 0, 1]], stim_channel='STI101')

                filename = str(file.split('.')[0])
                # Export the amended files back to .edf format
                mne.io.Raw.save(raw, filename[:-4] + '.raw.fif', overwrite=True)


tuep_preprocess(tuep_glob_path)
