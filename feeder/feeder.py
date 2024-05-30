# sys
import os
import sys
import numpy as np
import random
import pickle

# torch
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torchvision import datasets, transforms
from feeder.load_data import process_json_files, compare_strings
import pandas as pd
# visualization
import time

# operation
from . import tools

class Feeder(torch.utils.data.Dataset):
    """ Feeder for skeleton-based action recognition
    Arguments:
        data_path: the path to '.npy' data, the shape of data should be (N, C, T, V, M)
        label_path: the path to label
        random_choose: If true, randomly choose a portion of the input sequence
        random_shift: If true, randomly pad zeros at the begining or end of sequence
        window_size: The length of the output sequence
        normalization: If true, normalize input sequence
        debug: If true, only use the first 100 samples
    """

    def __init__(self, phase):
                 
        csv_path = "/media/dsp520/Grasp_2T/parkinson/GT.csv"
        json_path = "/media/dsp520/Grasp_2T/parkinson/LA/"

        csv = pd.read_csv (csv_path)
        # patients = np.zeros( (42, 700, 21) ) # 21 -> (3,7)
        patients = np.zeros( (42, 700, 25, 3) )
        level = [] # (42,)

        patients, GT = process_json_files (json_path, patients)
        # patients = np.transpose(patients, (0, 3, 2, 1)) # shape= (42, 3, 25, 700)
        patients = np.transpose(patients, (0, 3, 1, 2)) # shape= (42, 3, 700, 25)
        patients = np.expand_dims(patients, axis=4) # shape= (42, 3, 700, 25, 1)
        for i in range(GT.shape[0]):
            for j in range(csv.shape[0]):
                if compare_strings( GT[i], csv.iloc[j, 0] ):
                    level = np.append( level, csv.iloc[j, 1] )
                    break
        if phase=='train':
            self.label = level[:35]
            self.data  = patients[:35]
        elif phase=='test':
            self.label = level[35:]
            self.data = patients[35:]


    def __len__(self):
        return len(self.label)

    def __iter__(self):
        return self

    def __getitem__(self, index):
        # get data
        data_numpy = np.array(self.data[index])
        label = self.label[index]
        return data_numpy, label
