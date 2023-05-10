# BENDR 
*BErt-like Neurophysiological Data Representation*

![A picture of Bender from Futurama][logo]

This repository is a part of a Computer Science final year project. It is focused on replicating the results of the study on BENDR conducted by researchers at the University of Toronto. The link to the original paper is located below. 

[BENDR: using transformers and a contrastive self-supervised learning task to learn from massive amounts of EEG data](https://arxiv.org/pdf/2101.12037.pdf)

### ////////////// This text is a copy from the original BENDR github repo available here: https://github.com/SPOClab-ca/BENDR
To run these scripts, you will need to use the [DN3](https://dn3.readthedocs.io/en/latest/) project. We will try to keep this updated so that it works with the latest DN3 release. If you are just looking for the BENDR model, and don't need to reproduce the article results *per se*, BENDR will be (or maybe already is if I forgot to update it here) integrated into DN3, in which case I would start there.

Currently, we recommend version [0.2](https://github.com/SPOClab-ca/dn3/tree/v0.2-alpha). Feel free to open an issue if you are having any trouble.

More extensive instructions are upcoming, but in essence you will need to either:

    a)  Download the TUEG dataset and pre-train new encoder and contextualizer weights, _or_
    b)  Use the [pre-trained model weights](https://github.com/SPOClab-ca/BENDR/releases/tag/v0.1-alpha)
        
Once you have a pre-trained model:

    1) Add the paths of the pre-trained weights to configs/downstream.yml
    2) Edit paths to local copies of your datasets in configs/downstream_datasets.yml
    3) Run downstream.sh
    
### ////////////// End of the copied message

This repo is a copy of the original one that fixes some issues and allows for the training. In practice, you also need to swap two of the files from the dn3 library for the slighly modified versions provided in the modified_dn3_files directory. 

[logo]: BENDR-jacking-on.gif "Bender Jacking-on"
